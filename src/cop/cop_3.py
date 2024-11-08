import time
from pycsp3 import *
# import timeout
import json


# @timeout(600)
def generate_frequency_allocation_instance(fileName):
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

    emetteurs = VarArray(size=num_stations, dom=[data['stations'][i]['emetteur'] for i in range(num_stations)])
    recepteurs = VarArray(size=num_stations, dom=[data['stations'][i]['recepteur'] for i in range(num_stations)])

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

    minimize(
        Sum(emetteurs + recepteurs)
    )

    if solve() is SAT:
        es = values(emetteurs)
        rs = values(recepteurs)
        show_solution(es, rs, dic, num_regions)
    else:
        print("L'instance n'a pas de solution.")


def show_solution(es, rs, dic, num_regions):
    """
    Affiche la solution du d'allocation de fréquence COP.
    @param solution:
    """
    for j in range(num_regions):
        print(f"\nStations : {dic[j]}")
        print("em: ", [es[i] for i in dic[j]])
        print("rc: ", [rs[i] for i in dic[j]])
        print("delta:", [es[i] - rs[i] for i in dic[j]])


if __name__ == "__main__":
    startTime = time.time()
    generate_frequency_allocation_instance("../../donnees/donnees_cop/celar_50_7_10_5_0.800000_0.json")
    endTime = time.time()
    print(endTime - startTime, " s.")