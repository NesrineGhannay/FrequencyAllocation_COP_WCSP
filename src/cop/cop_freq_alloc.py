import argparse
import time
from pycsp3 import *
# import timeout
import json
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import signal


def resolve_instance(fileName, timeout, problem):
    """
    Génère une instance du problème des stations CSP et tente de trouver une solution.

    : param fileName:
    return:
    """
    with open(fileName, 'r') as file:
        data = json.load(file)
    # print(data)
    num_stations = len(data["stations"])
    num_regions = len(data["regions"])

    freqs_dom = []

    dic = {}
    for j in range(num_regions):
        dic[j] = []
    for i in range(num_stations):
        freqs_dom += data["stations"][i]["emetteur"] + data["stations"][i]["recepteur"]
        j = data["stations"][i]["region"]
        dic[j].append(i)

    # print(dic)
    # assert False
    freqs_dom = list(set(freqs_dom))  # occurrences uniques
    # print([0]+freqs_dom)
    # regions = VarArray(size=(len(data["regions"]), num_stations), dom=[0]+freqs_dom)

    emetteurs = VarArray(size=num_stations, dom=[data['stations'][i]['emetteur'] for i in range(num_stations)])
    recepteurs = VarArray(size=num_stations, dom=[data['stations'][i]['recepteur'] for i in range(num_stations)])
    # is_used = VarArray(size=max(freqs_dom), dom=[0, 1])
    satisfy(
        # distance entre fréquence émettrice et réceptrice d'une station
        [abs(emetteurs[i] - recepteurs[i]) == data["stations"][i]["delta"] for i in range(num_stations)],

        # distance entre fréquence de station proche
        [(abs(emetteurs[interference["x"]] - emetteurs[interference["y"]]) >= interference["Delta"]) &
         # (abs(emetteurs[interference["x"]] - recepteurs[interference["y"]]) >= interference["Delta"]) &
         # (abs(recepteurs[interference["x"]] - emetteurs[interference["y"]]) >= interference["Delta"]) &
         (abs(recepteurs[interference["x"]] - recepteurs[interference["y"]]) >= interference["Delta"])
         for interference in data["interferences"]],

        # limiter le nombre de fréquences utilisé par station
        [
            NValues([emetteurs[j] for j in range(num_stations) if data["stations"][j]["region"] == i]) +
            NValues([recepteurs[j] for j in range(num_stations) if data["stations"][j]["region"] == i]) <=
            data["regions"][i]
            for i in range(len(data["regions"]))
        ]

    )

    if problem == 1:
        minimize(
            NValues(emetteurs + recepteurs)
        )
    elif problem == 2:
        minimize(
            Sum(recepteurs + emetteurs)
        )
    else:
        minimize(
            abs(Maximum(emetteurs + recepteurs) - Minimum(emetteurs + recepteurs))
        )

    """solvers = [ACE]
    for s in solvers:
        print(f"Essai avec le solveur {s}:")"""
    if solve(options=f"-t={timeout}s") is OPTIMUM:
        # print(NValues(regions[i] for i in range(num_regions)))
        es = values(emetteurs)
        rs = values(recepteurs)
        # reg = values(regions)
        # print([f for f, value in enumerate(values(is_used)) if value == 1])
        # show_solution(es, rs, dic, num_regions, data)
        if problem == 1:
            unique_es = len(set(es))
            unique_rs = len(set(rs))
            #print(f"fonction objectif: {es}, {rs}")
            print(f"Nombre d'occurrences uniques de es: {unique_es}")
            print(f"Nombre d'occurrences uniques de rs: {unique_rs}")
        elif problem == 2:
            print(f"fonction objectif: {sum(es) + sum(rs)}")
        else:
            print(f"fonction objectif: {abs(max(es + rs) - min(es + rs))}")
    else:
        print(f"L'instance n'a pas de solution.{problem}")


def show_solution(es, rs, dic, num_regions, data):
    """
    Affiche la solution du d'allocation de fréquence COP.
    @param solution:
    """
    for j in range(num_regions):
        print(f"\n== Région {j} ==")
        for i in dic[j]:
            print(f"Station {i}: em: {es[i]}, rc: {rs[i]}, delta: {es[i] - rs[i]} < {data['stations'][i]['delta']}")
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('file_name', type=str, help='The name of the file to process')
    parser.add_argument('--timeout', type=int, default=60, help='The timeout for the resolution')
    parser.add_argument("--problem", type=int, default=1, help="The problem to solve")

    args = parser.parse_args()
    file_name = args.file_name
    timeout = args.timeout
    problem = args.problem
    resolve_instance(file_name, timeout, problem)
