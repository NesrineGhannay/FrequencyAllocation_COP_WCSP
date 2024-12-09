import argparse
import time
from pycsp3 import *
import json
import os


def resolve_instance(fileName, timeout, problem, solver):
    """
    Génère une instance du problème des stations COP et tente de trouver une solution.

    Paramètres :
        fileName (str) : Nom du fichier contenant les données au format JSON
        timeout (int) : Limite de temps de résolution d'une instance
        problem (int) : Numéro du problème à résoudre
            (1: minimisation du nombre de fréquence utilisées,
            2: utilisation des fréquences les plus basses,
            3 : minimiser la largeur de la bande de fréquence)
        solver (str) : Solver pour la résolution de l'instance (ACE ou CHOCO)

    Return :
        int : Valeur de la fonction objectif
        float : Durée d'exécution
        tuple : Fréquences émettrices et réceptrices
    """
    with open(fileName, 'r') as file:
        data_cop = json.load(file)

    num_stations = len(data_cop["stations"])
    liaisons = data_cop["liaisons"]

    # Définition des variables du problème
    emetteurs = VarArray(size=num_stations, dom=[data_cop['stations'][i]['emetteur'] for i in range(num_stations)])
    recepteurs = VarArray(size=num_stations, dom=[data_cop['stations'][i]['recepteur'] for i in range(num_stations)])

    # Définition des contraintes
    satisfy(
        # distance entre fréquence émettrice et réceptrice d'une station
        [abs(emetteurs[i] - recepteurs[i]) == data_cop["stations"][i]["delta"] for i in range(num_stations)],

        # distance entre fréquence de station proche
        [(abs(emetteurs[interference["x"]] - emetteurs[interference["y"]]) >= interference["Delta"]) &
         (abs(recepteurs[interference["x"]] - recepteurs[interference["y"]]) >= interference["Delta"])
         for interference in data_cop["interferences"]],

        # limiter le nombre de fréquences utilisé par station
        [
            NValues([emetteurs[j] for j in range(num_stations) if data_cop["stations"][j]["region"] == i]) +
            NValues([recepteurs[j] for j in range(num_stations) if data_cop["stations"][j]["region"] == i]) <=
            data_cop["regions"][i]
            for i in range(len(data_cop["regions"]))
        ],

        # liaisons entre fréquences émettrices et réceptrices
        [emetteurs[l["x"]] == recepteurs[l["y"]] for l in liaisons],
        [emetteurs[l["y"]] == recepteurs[l["x"]] for l in liaisons]
    )

    if problem == 1:  # minimiser le nombre total de fréquences utilisées
        minimize(
            NValues(emetteurs + recepteurs)
        )
    elif problem == 2:  # utiliser les fréquences les plus basses
        minimize(
            Maximum(emetteurs + recepteurs)
        )
    else:  # minimiser la largeur de la bande de fréquence
        minimize(
            abs(Maximum(emetteurs + recepteurs) - Minimum(emetteurs + recepteurs))
        )

    options = f"-t={timeout}s"
    if solver == "CHOCO":
        options = f"-limit={timeout}s"

    start = time.time()
    if solve(solver=solver, options=options) is OPTIMUM:
        exe_duration = time.time() - start
        es = values(emetteurs)
        rs = values(recepteurs)

        # Récupération de la valeur de la fonction objectif et des autres informations comme les fréquences utilisées
        # ainsi que le temps d'exécution
        if problem == 1:
            return len(set(rs + es)), exe_duration, (es, rs)
        elif problem == 2:
            s = 0
            for em_i in set(es):
                s += em_i
            for rc_i in set(rs):
                s += rc_i
            return max(es + rs), exe_duration, (es, rs)
        else:
            length = abs(max(es + rs) - min(es + rs))
            return length, exe_duration, (es, rs)
    else:
        exe_duration = time.time() - start
        print(f"L'instance n'a pas de solution!")
        return None, exe_duration, None


def generate_instance_and_solution(filename, timeout, problem, solver):
    """
    Génère une instance du problème des stations COP et lance la résolution.
    Cette fonction génère un fichier XML contenant l'instance et un fichier texte contenant la solution.

    Paramètres :
    filename (str) : Nom du fichier contenant les données au format JSON
    timeout (int) : Limite de temps de résolution d'une instance en secondes
    problem (int) : Numéro du problème à résoudre
        (1: minimisation du nombre de fréquences utilisées,
        2: utilisation des fréquences les plus basses,
        3 : minimiser la largeur de la bande de fréquence)
    solver (str) : Solveur à utiliser (ACE ou CHOCO)

    Return :
    None
    """
    print(f"Résolution de l'instance {filename}, problème {problem} et solveur = {solver}")
    objectif_value, d, sol = resolve_instance(filename, timeout, problem, solver)
    if sol is None:
        with open(f"src/cop/solutions/{problem}/{filename.split('/')[-1].replace('.json', '.txt')}", "w") as file:
            file.write(f"L'instance n'a pas de solution.\n")
            file.write(f"Durée d'exécution: {d} secondes\n\n, Solveur: {solver}\n")
        return
    # Création du fichier XML correspondant en renommant le fichier généré automatiquement par pycsp3
    os.rename("cop_freq_alloc.xml", f"src/cop/instances/{problem}/{filename.split('/')[-1].replace('.json', '.xml')}")
    es, rs = sol
    with open(f"src/cop/solutions/{problem}/{filename.split('/')[-1].replace('.json', '.txt')}", "w") as file:
        file.write(f"Valeur de la fonction objectif: {objectif_value}\n")
        file.write(f"Fréquences utilisées: {set(es + rs)}\n")
        file.write(f"Durée d'exécution: {d} secondes\n\n, Solveur: {solver}\n")
        with open(filename, 'r') as f:
            data_cop = json.load(f)
            liaisons = data_cop["liaisons"]
            for l in liaisons:
                file.write(f"Liaison entre la station {l['x']} et la station {l['y']}\n")
                file.write(f"em de {l['x']} --> rc de {l['y']}: {es[l['x']]} == {rs[l['y']]}\n")
                file.write(f"em de {l['y']} --> rc de {l['x']}: {es[l['y']]} == {rs[l['x']]}\n\n")
        for i in range(len(es)):
            file.write(f"Station {i}: em: {es[i]}, rc: {rs[i]}, delta: {abs(es[i] - rs[i])}\n")


def main():
    # Parsing des arguments
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('file_name', type=str, help='The name of the file to process')
    parser.add_argument('--timeout', type=int, default=60, help='The timeout for the resolution')
    parser.add_argument("--problem", type=int, default=1, help="The problem to solve : 1, 2 or 3")
    parser.add_argument("--solver", type=str, default="ACE", help="The solver to use : ACE or CHOCO")

    args = parser.parse_args()
    file_name = args.file_name
    timeout = args.timeout
    problem = args.problem
    solver = args.solver

    # Appel de la fonction de résolution
    generate_instance_and_solution(file_name, timeout, problem, solver)


if __name__ == "__main__":
    main()
