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
    emetteurs = VarArray(size=num_stations, dom=[data['stations'][i]['emetteur'] for i in range(num_stations)])
    recepteurs = VarArray(size=num_stations, dom=[data['stations'][i]['recepteur'] for i in range(num_stations)])
    is_used = VarArray(size=num_stations, dom=[0, 1])
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
        # [is_used[i]==1 if emetteurs[i]==14 else 0 for i in range(num_stations)]
    )

    # Minimiser le nombre de fréquences utilisé
    """minimize(
        NValues(emetteurs) + NValues(recepteurs)
    )"""

    if solve() is SAT:
        es = values(emetteurs)
        rs = values(recepteurs)
        show_solution(es, rs)
    else:
        print("L'instance n'a pas de solution.")
        return "NO SOLUTION"


def show_solution(es, rs):
    """
    Affiche la solution du d'allocation de fréquence COP.
    @param solution:
    """
    for i in range(len(es)):
        print(f"{i}: e:{es[i]}, r:{rs[i]}")


if __name__ == "__main__":
    startTime = time.time()
    generate_frequency_allocation_instance("../../donnees/donnees_cop/celar_50_7_10_5_0.800000_0.json")
    endTime = time.time()
    print(endTime - startTime, " s.")
