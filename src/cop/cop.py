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

    ############# Idée de modélisation du problème 1 #############
    # Récupération d'une liste contenant toutes les valeurs possibles qu'une fréquence peut prendre
    freqs_dom = []
    for i in range(num_stations):
        freqs_dom += data["stations"][i]["emetteur"] + data["stations"][i]["recepteur"]
    freqs_dom = list(set(freqs_dom))  # occurrences uniques

    dic_freq_id = {}  # dictionnaires qui associera à chaque fréquence un indice
    for j in range(len(freqs_dom)):
        dic_freq_id[freqs_dom[j]] = j
    print(dic_freq_id)

    # list de variables qui vérifient si une fréquence est utilisé ou pas
    is_freq_used = VarArray(size=len(freqs_dom), dom=[0, 1])
    ##############################################################

    emetteurs = VarArray(size=num_stations, dom=[data["stations"][i]["emetteur"] for i in range(num_stations)])
    recepteurs = VarArray(size=num_stations, dom=[data["stations"][i]["recepteur"] for i in range(num_stations)])

    satisfy(
        [abs(emetteurs[i] - recepteurs[i]) == data["stations"][i]["delta"] for i in range(num_stations)],  # manquait le i
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


def minimize_num_frequencies(e, r, f, dic_feq_id):
    """
    Prends deux Varray correspondant aux fréquences émettrices et récepteurs
    et retourne une solution qui minimize le nombre de fréquences utilisé
    """
    # TODO: soit définir une nouvelle VarArray booléenne qui vaut vrai si une fréquence est utilisé et minimise la somme

    satisfy(
        [f[dic_feq_id[e_i]] == 1 for e_i in e],  # pas correct (génère une erreur)
        [f[dic_feq_id[r_i]] == 1 for r_i in r]   # same
    )

    minimize(
        Sum(f)
    )

    if solve() is SAT:
        print(f"1 : Solution trouvée :\nÉmetteurs: {e.values()}\nRécepteurs: {r.values()}")
        return

    else:
        print("1 : L'instance n'a pas de solution.")
        return "NO SOLUTION"

if __name__ == "__main__":
    startTime = time.time()
    valeurs = generate_frequency_allocation_instance("donnees/donnees_cop/celar_50_7_10_5_0.800000_0.json")
    endTime = time.time()
    print(endTime - startTime, " s.")

    if valeurs != "NO SOLUTION":
        show_solution(valeurs)