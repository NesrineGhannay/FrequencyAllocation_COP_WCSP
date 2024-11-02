import time
from pycsp3 import *
# import timeout
import json
import re

def generate_wcsp_from_json(input_file):
    """
    Génère une instance du problème d'allocation de fréquence au format WCSP/CFN à partir d'un fichier JSON.

    :param input_file: Nom du fichier JSON d'entrée.
    """
    with open(input_file, 'r') as f:
        data = json.load(f)

    nb_vars = len(data["stations"]) * 2
    domain_size = sum(len(station['emetteur']) for station in data['stations']) * 2
    nb_constraints = len(data["stations"]) + len(data["interferences"]) + len(data["regions"])
    max_cost = 1000

    output_file = re.sub("celar", "frequency_allocation", input_file)

    with open(output_file, 'w') as f:
        f.write(
            f"frequency_allocation {nb_vars} {domain_size} {nb_constraints} {max_cost}\n") # pas sûre encore

        # Définition des variables et de leur domaine
        var_id = 0
        for station in data["stations"]:

            emetteur_domain = station["emetteur"]
            recepteur_domain = station["recepteur"]

            # proposition 1
            f.write(f"{var_id} {len(emetteur_domain)} " + " ".join(map(str, emetteur_domain)) + "\n")
            var_id += 1
            f.write(f"{var_id} {len(recepteur_domain)} " + " ".join(map(str, recepteur_domain)) + "\n")
            var_id += 1

            # proposition 2
            # f.write(f"{len(emetteur_domain)}\n")  # Taille du domaine pour l'émetteur
            # f.write(f"{len(recepteur_domain)}\n")

        ################# Fonction de coût #################

        # contraintes d'écart entre émetteur et récepteur pour chaque station
        var_id = 0
        for station in data["stations"]:
            delta = station["delta"]
            ...

        # contraintes d'interférence entre stations proches
        for interference in data["interferences"]:
            x, y, delta_xy = interference["x"], interference["y"], interference["Delta"]
            ...

        # contraintes du nombre de fréquences par région
        for station in data["stations"]:
            ...

    print(f"WCSP file generated: {output_file}")

# generate_wcsp_from_json("celar_50_7_10_5_0.800000_0.json")

