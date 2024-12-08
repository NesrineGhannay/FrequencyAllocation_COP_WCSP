import json
import argparse
import pytoulbar2 as tb2
import multiprocessing
import os
import time


class WCSPProblem:
    def __init__(self, json_file, wcsp_file, max_cost=1000, evaluation_function="proportional"):
        """
        Initialise le problème WCSP.
        """
        self.json_file = json_file
        self.wcsp_file = wcsp_file
        self.max_cost = max_cost
        self.evaluation_function = evaluation_function
        self.dic_freq_id = {}
        self.constraints = []
        self.domains = []
        self.variables = []
        self.variable_indices = {}

    
    def generate_wcsp_file(self):
        """
        Génère un fichier WCSP à partir des données JSON.
        """
        with open(self.json_file, 'r') as file:
            data = json.load(file)

        num_stations = len(data["stations"])
        interferences = data["interferences"]
        liaisons = data["liaisons"]

        # Calculs des couts
        self.max_cost = 10 * len(data["stations"])
        liaisons_cost = int(0.2 * self.max_cost)
        print("Coût maximal autorisé : ", self.max_cost)

        frequencies = []
        for i in range(num_stations):
            frequencies += data["stations"][i]["emetteur"] + data["stations"][i]["recepteur"]
        frequencies = list(set(frequencies))
        self.dic_freq_id = {freq: idx for idx, freq in enumerate(frequencies)}
        print(f"Dictionnaire d'indices : {self.dic_freq_id}")

        # Contraintes de matériel
        for i, station in enumerate(data["stations"]):
            emetteur_var = len(self.variables)
            recepteur_var = len(self.variables) + 1

            self.variable_indices[f"emetteur_{i}"] = emetteur_var
            self.variable_indices[f"recepteur_{i}"] = recepteur_var
            self.variables.extend([emetteur_var, recepteur_var])
            self.domains.extend([len(frequencies), len(frequencies)])

            # Contrainte 1 : |emetteur - recepteur| >= delta
            delta = station["delta"]
            tuples = []

            for e in station["emetteur"]:
                for r in station["recepteur"]:
                    if abs(e - r) == delta:
                        tuples.append((self.dic_freq_id[e], self.dic_freq_id[r], 0)) 
                    else:
                        tuples.append((self.dic_freq_id[e], self.dic_freq_id[r], self.max_cost))

            self.constraints.append({
                "arity": 2,
                "scope": [emetteur_var, recepteur_var],
                "default_cost": self.max_cost, 
                "tuples": tuples,
            })

        # Contraintes d'interférences
        for interference in interferences:
            x, y = interference["x"], interference["y"]
            delta_min = interference["Delta"]

            emetteur_x, emetteur_y = self.variable_indices[f"emetteur_{x}"], self.variable_indices[f"emetteur_{y}"]
            recepteur_x, recepteur_y = self.variable_indices[f"recepteur_{x}"], self.variable_indices[f"recepteur_{y}"]

            # Émetteurs
            tuples = []
            for ex in data["stations"][x]["emetteur"]:
                for ey in data["stations"][y]["emetteur"]:
                    if abs(ex - ey) < delta_min:
                        violation_cost = int(0.1 * self.max_cost * abs(delta_min - abs(ex - ey))) 
                        tuples.append((self.dic_freq_id[ex], self.dic_freq_id[ey], violation_cost))
                    else:
                        tuples.append((self.dic_freq_id[ex], self.dic_freq_id[ey], 0))

            self.constraints.append({
                "arity": 2,
                "scope": [emetteur_x, emetteur_y],
                "default_cost": self.max_cost,
                "tuples": tuples,
            })

            # Récepteurs
            tuples = []
            for rx in data["stations"][x]["recepteur"]:
                for ry in data["stations"][y]["recepteur"]:
                    if abs(rx - ry) < delta_min:
                        violation_cost = int(0.1 * self.max_cost * abs(delta_min - abs(rx - ry)))
                        tuples.append((self.dic_freq_id[rx], self.dic_freq_id[ry], violation_cost))
                    else:
                        tuples.append((self.dic_freq_id[rx], self.dic_freq_id[ry], 0))

            self.constraints.append({
                "arity": 2,
                "scope": [recepteur_x, recepteur_y],
                "default_cost": self.max_cost,
                "tuples": tuples,
            })

        # Contraintes de liaison directe
        for liaison in liaisons:
            x, y = liaison["x"], liaison["y"]

            emetteur_x, recepteur_y = self.variable_indices[f"emetteur_{x}"], self.variable_indices[f"recepteur_{y}"]
            emetteur_y, recepteur_x = self.variable_indices[f"emetteur_{y}"], self.variable_indices[f"recepteur_{x}"]

            tuples = []
            for ex in data["stations"][x]["emetteur"]:
                for ry in data["stations"][y]["recepteur"]:
                    if ex != ry:
                        tuples.append((self.dic_freq_id[ex], self.dic_freq_id[ry], liaisons_cost))
                    else:
                        tuples.append((self.dic_freq_id[ex], self.dic_freq_id[ry], 0))

            self.constraints.append({
                "arity": 2,
                "scope": [emetteur_x, recepteur_y],
                "default_cost": 50,
                "tuples": tuples,
            })

        with open(self.wcsp_file, 'w') as file:
            file.write(f"freq_alloc {len(self.variables)} {max(self.domains)} {len(self.constraints)} 1000\n")
            file.write(f"{' '.join(map(str, self.domains))}\n")

            for constraint in self.constraints:
                scope = ' '.join(map(str, constraint["scope"]))
                file.write(f"{constraint['arity']} {scope} {constraint['default_cost']} {len(constraint['tuples'])}\n")
                for t in constraint["tuples"]:
                    file.write(f"{' '.join(map(str, t[:-1]))} {t[-1]}\n")

        print(f"WCSP file '{self.wcsp_file}' generated successfully!")


    def solve_wcsp(self, max_time=600):
        """
        Résout une instance WCSP avec PyToulbar2 et traduit les indices en fréquences d'origine.
        Sauvegarde la solution trouvée ou le statut dans un fichier dédié.

        Paramètres :
            max_time (int) : Temps maximal pour la résolution (en secondes).
        """
        filepath = os.path.basename(self.wcsp_file)
        filename = os.path.splitext(filepath)[0]
        output_filename = f"src/vcsp/solutions/{filename}.txt"

        def solve():
            nonlocal start_time, elapsed_time, solution_found, solution_cost
            try:
                start_time = time.time()
                cfn = tb2.CFN()
                cfn.Read(self.wcsp_file)
                solution_cost = cfn.Solve(showSolutions=3, timeLimit=max_time)
                elapsed_time = time.time() - start_time
                if solution_cost is not None:
                    solution_found = True
                    solution_values, total_cost, _ = solution_cost

                    print("Solution brute trouvée :", solution_values)

                    try:
                        solution = []
                        for i in range(0, len(solution_values), 2):
                            emetteur_freq = solution_values[i]
                            recepteur_freq = solution_values[i + 1]

                            emetteur_orig = [key for key, val in self.dic_freq_id.items() if val == emetteur_freq]
                            recepteur_orig = [key for key, val in self.dic_freq_id.items() if val == recepteur_freq]

                            if emetteur_orig and recepteur_orig:
                                solution.append((emetteur_orig[0], recepteur_orig[0]))
                            else:
                                raise KeyError(f"Indice de fréquence introuvable : {emetteur_freq}, {recepteur_freq}")

                        with open(output_filename, "w") as file:
                            file.write(f"Solution trouvée avec un coût total de : {total_cost}\n")
                            file.write(f"Temps d'exécution : {elapsed_time:.2f} secondes\n")
                            file.write("Station -> Fréquence Émettrice / Fréquence Réceptrice\n")
                            for station_id, (freq_em, freq_rec) in enumerate(solution):
                                file.write(f"Station {station_id} -> {freq_em} / {freq_rec}\n")
                        print("-------------------------------------------------------")
                        print(f"Solution trouvée avec un coût total de : {total_cost}")
                        print(f"Temps d'exécution : {elapsed_time:.2f} secondes")
                        print(f"Solution sauvegardée dans le fichier : {output_filename}")
                        print("-------------------------------------------------------")

                    except KeyError as e:
                        print(f"Erreur : clé introuvable dans le dictionnaire des fréquences ({e}).")
                        with open(output_filename, "w") as file:
                            file.write("Erreur pendant la résolution : clé introuvable dans le dictionnaire des fréquences.\n")
                            file.write(f"Clé problématique : {e}\n")
                else:
                    with open(output_filename, "w") as file:
                        file.write("Aucune solution trouvée.\n")
                    print(f"Aucune solution trouvée. Résultats sauvegardés dans : {output_filename}")

            except Exception as e:
                elapsed_time = time.time() - start_time
                solution_found = False
                with open(output_filename, "w") as file:
                    file.write(f"Erreur pendant la résolution : {str(e)}\n")
                print(f"Erreur pendant la résolution : {e}")

        start_time = 0
        elapsed_time = 0
        solution_found = False
        solution_cost = None

        process = multiprocessing.Process(target=solve)
        process.start()
        process.join(timeout=max_time)

        if process.is_alive():
            process.terminate()
            process.join()
            elapsed_time = max_time
            with open(output_filename, "w") as file:
                file.write(f"Temps d'exécution dépassé ({max_time} secondes). Résolution interrompue.\n")
            print(f"Temps d'exécution dépassé ({max_time} secondes). Résolution interrompue.")

def main():
    parser = argparse.ArgumentParser(description="Création et résolution d'une instance WCSP.")
    parser.add_argument("json_file", type=str, help="Chemin vers le fichier JSON d'entrée.")
    parser.add_argument("wcsp_file", type=str, help="Chemin vers le fichier WCSP de sortie.")
    parser.add_argument("--max_time", type=int, default=600, help="Temps maximal pour la résolution (en secondes).")
    parser.add_argument("--max_cost", type=int, default=1000, help="Coût maximal pour les contraintes non respectées.")
    parser.add_argument("--evaluation_function", type=str, choices=["proportional", "quadratic", "constant"], default="proportional",
                        help="Fonction d'évaluation pour les contraintes simples.")

    args = parser.parse_args()

    problem = WCSPProblem(
        json_file=args.json_file,
        wcsp_file=args.wcsp_file,
        max_cost=args.max_cost,
        evaluation_function=args.evaluation_function
    )

    problem.generate_wcsp_file()
    problem.solve_wcsp()



if __name__ == "__main__":
    main()