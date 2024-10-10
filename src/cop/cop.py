import time
from pycsp3 import *
import timeout
import json


@timeout(600)
def generate_frequency_allocation_instance(fileName):
    """
    Génère une instance du problème des stations CSP et tente de trouver une solution.

    : param fileName:
    return:
    """
    with open(fileName, 'r') as file:
        data = json.load(file)
    print(data)

    num_stations = len(data["stations"])
    # regions = VarArray(size=num_stations, dom=[data["stations"][i]["region"] for i in range(num_stations)])
    emetteurs = VarArray(size=num_stations, dom=[data["stations"][i]["emetteur"] for i in range(num_stations)])
    recepteurs = VarArray(size=num_stations, dom=[data["stations"][i]["recepteur"] for i in range(num_stations)])

    satisfy(
        [abs(emetteurs[i] - recepteurs[i]) == data["stations"]["delta"] for i in range(num_stations)],
        [(abs(emetteurs[interference["x"]] - emetteurs[interference["y"]]) >= interference["Delta"])
         for interference in data["interferences"]],

        # Limiter le nb de stations par région

    )

    minimize(
        Sum([emetteurs[i] + recepteurs[i] for i in range(num_stations)]),
        # Maximum([regions[i], (emetteurs[i]) for i in range(num_stations)]),
        # Sum([regions[i] * (emetteurs[i] + recepteurs[i]) for i in range(num_stations)])
    )

    if solve() is SAT:
        print(f"Solution trouvée :\nÉmetteurs: {emetteurs.values()}\nRécepteurs: {recepteurs.values()}")
        return

    else:
        print("L'instance n'a pas de solution.")
        return "NO SOLUTION"


def show_solution(solution):
    """
    Affiche la solution du d'allocation de fréquence COP.
    @param solution:
    """

    return


if __name__ == "__main__":
    startTime = time.time()
    valeurs = generate_frequency_allocation_instance("donnees/donnees_cop/celar_50_7_10_5_0.800000_0.json")
    endTime = time.time()
    print(endTime - startTime, " s.")

    if valeurs != "NO SOLUTION":
        show_solution(valeurs)