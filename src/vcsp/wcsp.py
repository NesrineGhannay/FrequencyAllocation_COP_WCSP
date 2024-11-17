import json

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

    variables = []
    domains = []
    constraints = []

    variable_indices = {}
    for i, station in enumerate(data["stations"]):
        emetteur_var = len(variables)
        recepteur_var = len(variables) + 1

        variable_indices[f"emetteur_{i}"] = emetteur_var
        variable_indices[f"recepteur_{i}"] = recepteur_var
        variables.append(emetteur_var)
        variables.append(recepteur_var)
        domains.append(station["emetteur"])
        domains.append(station["recepteur"])

        # |emetteur - recepteur| == delta
        delta = station["delta"]
        tuples = [
            (e, r, 0)
            for e in station["emetteur"]
            for r in station["recepteur"]
            if abs(e - r) == delta
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
            (ex, ey, 0)
            for ex in domains[emetteur_x]
            for ey in domains[emetteur_y]
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
            (rx, ry, 0)
            for rx in domains[recepteur_x]
            for ry in domains[recepteur_y]
            if abs(rx - ry) >= delta_min
        ]
        constraints.append({
            "arity": 2,
            "scope": [recepteur_x, recepteur_y],
            "default_cost": max_cost,
            "tuples": tuples,
        })

    with open(wcsp_file, 'w') as file:
        file.write(f"frequency_allocation {len(variables)} {max(len(d) for d in domains)} {len(constraints)} 1000\n")

        for domain in domains:
            file.write(f"{len(domain)} {' '.join(map(str, domain))}\n")

        for constraint in constraints:
            scope = ' '.join(map(str, constraint["scope"]))
            file.write(f"{constraint['arity']} {scope} {constraint['default_cost']} {len(constraint['tuples'])}\n")
            for t in constraint["tuples"]:
                file.write(f"{' '.join(map(str, t[:-1]))} {t[-1]}\n")

    print(f"WCSP file '{wcsp_file}' generated successfully!")


json_file = "../../donnees/donnees_wcsp/celar_50_7_10_5_0.800000_0.json"
wcsp_file = "output.wcsp"
generate_wcsp_file(json_file, wcsp_file)
