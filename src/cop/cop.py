import time
from pycsp3 import *
import timeout
import json


def generate_frequency_allocation_instance(fileName):
    """
    Génère une instance du problème des stations CSP et tente de trouver une solution.

    : param fileName:
    return:
    """
    with open(fileName, 'r') as file:
        data = json.load(file)

    # emeteurs = VarArray(size=data["station"]["emetteur"], dom=range(1, k + 1))
    # recepeteur =

    satisfy(

    )

    minimize(

    )

    # Résout le problème CSP
    if solve() is SAT:
        return
    else:
        print("L'instance n'a pas de solution")
        return "NO SOLUTION"


def show_solution(solution):
    """
    Affiche la solution du d'allocation de fréquence COP.
    :param solution:
    """

    return


if __name__ == "__main__":
    startTime = time.time()
    valeurs = generate_frequency_allocation_instance("donnees/donnees_cop/celar_50_7_10_5_0.800000_0.json")
    endTime = time.time()
    print(endTime - startTime, " s.")

    if valeurs != "NO SOLUTION":
        show_solution(valeurs)