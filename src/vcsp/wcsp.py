import json
import pytoulbar2

def generate_wcsp_file(json_file, wcsp_file, max_cost=1000):
    """
    Génère un fichier WCSP à partir des données JSON pour un problème d'allocation de fréquences.

    Paramètres :
        json_file (str) : Chemin vers le fichier JSON contenant les données.
        wcsp_file (str) : Chemin du fichier WCSP à générer.
    """
    with open(json_file, 'r') as file:
        data = json.load(file)

    num_stations = len(data["stations"])
    interferences = data["interferences"]

    constraints = []
    domains = []

    frequencies = []
    for i in range(num_stations):
        frequencies += data["stations"][i]["emetteur"] + data["stations"][i]["recepteur"]
    frequencies = list(set(frequencies))  # occurrences uniques
    dic_freq_id = {}  # dictionnaires qui associera à chaque fréquence un indice
    for j in range(len(frequencies)):
        dic_freq_id[frequencies[j]] = j
    print(dic_freq_id)

    variables = []
    variable_indices = {}

    for i, station in enumerate(data["stations"]):
        emetteur_var = len(variables)
        recepteur_var = len(variables) + 1

        variable_indices[f"emetteur_{i}"] = emetteur_var
        variable_indices[f"recepteur_{i}"] = recepteur_var
        variables.append(emetteur_var)
        variables.append(recepteur_var)

        domains.append(len(frequencies))
        domains.append(len(frequencies))

        delta = station["delta"]
        tuples = [
            (dic_freq_id[e], dic_freq_id[r], 0)  # on utilise les indices associées aux fréquences
            for e in station["emetteur"]
            for r in station["recepteur"]
            if abs(e - r) >= delta
        ]
        constraints.append({
            "arity": 2,
            "scope": [emetteur_var, recepteur_var],
            "default_cost": max_cost,
            "tuples": tuples,
        })

    for interference in interferences:
        x = interference["x"]
        y = interference["y"]
        delta_min = interference["Delta"]

        emetteur_x = variable_indices[f"emetteur_{x}"]
        emetteur_y = variable_indices[f"emetteur_{y}"]

        tuples = [
            (dic_freq_id[ex], dic_freq_id[ey], 0)
            for ex in data["stations"][x]["emetteur"]
            for ey in data["stations"][y]["emetteur"]
            if abs(ex - ey) >= delta_min
        ]
        constraints.append({
            "arity": 2,
            "scope": [emetteur_x, emetteur_y],
            "default_cost": max_cost,
            "tuples": tuples,
        })

        recepteur_x = variable_indices[f"recepteur_{x}"]
        recepteur_y = variable_indices[f"recepteur_{y}"]

        tuples = [
            (dic_freq_id[rx], dic_freq_id[ry], 0)
            for rx in data["stations"][x]["emetteur"]
            for ry in data["stations"][y]["emetteur"]
            if abs(rx - ry) >= delta_min
        ]
        constraints.append({
            "arity": 2,
            "scope": [recepteur_x, recepteur_y],
            "default_cost": delta_min,
            "tuples": tuples,
        })

    with open(wcsp_file, 'w') as file:
        file.write(f"frequency_allocation {len(variables)} {max(domains)} {len(constraints)} 1000\n")

        file.write(f"{' '.join([str(d) for d in domains])}")

        for constraint in constraints:
            scope = ' '.join(map(str, constraint["scope"]))
            file.write(f"{constraint['arity']} {scope} {constraint['default_cost']} {len(constraint['tuples'])}\n")
            for t in constraint["tuples"]:
                file.write(f"{' '.join(map(str, t[:-1]))} {t[-1]}\n")

    print(f"WCSP file '{wcsp_file}' generated successfully!")


json_file = "../../donnees/donnees_wcsp/celar_50_7_10_5_0.800000_0.json"
wcsp_file = "output.wcsp"
generate_wcsp_file(json_file, wcsp_file)
