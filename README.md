# **Projet : Résolution de Problèmes d'Allocation de Fréquences entre Stations**

> **Auteur :** Nesrine GHANNAY  & Kossi KOSSIVI
>
> **Master 2 :** Informatique, spécialité Intelligence Artificielle et Apprentissage Automatique (IAAA)  
>
> **Université :** Aix-Marseille Université  
> _Encadré par Cyril TERRIOUX_  
---

## **Description du Projet**

Ce projet explore des méthodes avancées pour résoudre des problèmes d'**allocation de fréquences** entre différentes stations, en minimisant les interférences et en respectant des contraintes spécifiques. Deux approches principales sont utilisées :  
1. **Les problèmes d'optimisation sous contraintes (COP)** : modélisés et résolus avec ACE et CHOCO.  
2. **Les problèmes de satisfaction de contraintes valuées (WCSP)** : modélisés et résolus avec Toulbar2.  

---

## **Organisation du Projet**
### **Répertoires et Fichiers**
- **`donnees/`**  
  Contient les fichiers d'entrée nécessaires pour les expérimentations.  

  - **`donnees_cop/`** : Instances du problème en format compatible avec ACE et CHOCO.  
  - **`donnees_wcsp/`** : Instances WCSP pour Toulbar2.  

- **`src/`**  
  Regroupe les scripts pour modéliser et résoudre les problèmes :
  - **`cop/`** : Dossier où se trouve le code nécessaire pour modéliser et résoudre les instances COP.  
    - **`solutions/`** : Répertoire où se trouve le résultat de chaque résolution faites avec COP. Il contient trois sous-répertoires :
      - **`1/`** : Répertoire où se trouve le résultat de chaque résolution pour le problème de minimisation du nombre de fréquences utilisées.
      - **`2/`** : Répertoire où se trouve le résultat de chaque résolution pour le problème d'utilisation des fréquences les plus basses.
      - **`3/`** : Répertoire où se trouve le résultat de chaque résolution pour le problème de minimisation de la bande des fréqunces utilisées.
    - **`instances/`** : Répertoire contenant les instances au format xml générées par le script `scop_freq_alloc.py`.
    - **`scop_freq_alloc.py`** : Script principal pour modéliser et résoudre les instances COP.
  Il faut noter que les solutions contenues dans les répertoires listés précédemment ont été obtenues en utilisant le solveur ACE
  - **`vcsp/`** : Dossier où se trouve le code nécessaire pour modéliser et résoudre les instances WCSP, ainsi que les fichiers générés pour et par Toulbar2.
    - **`solutions/`** : Répertoire où se trouve le résultat de chaque résolution faites avec WCSP.
    - **`instances/`** : Répertoire contenant les instances au format WCSP générées par le script `wcsp.py` pour la résolution par Toolbar2.
    - **`wcsp.py`** : Script Python pour générer et résoudre les instances WCSP avec la bibliothèque `pytoulbar2`.

- **`run_cop.sh`**  
  Script Bash pour lancer les solveurs sur les instances COP et enregistrer les résultats dans les fichiers correspondants.

- **`wcsp_experiments.ipynb`**  
  Notebook pour expérimenter avec les méthodes WCSP, incluant la visualisation des performances.

---

## **Comment Utiliser**

### **Prérequis**
Installer Python et les librairies nécessaires :  
   ```bash
   pip install pycsp3 pytoulbar2
   ```
### **Résolution COP**
Pour résoudre les instances fournies dans le répertoire **`donnees_cop/`** il faut utiliser le script **`run_cop.sh`**
qui permet de lancer la résolution en série des instances COP avec ACE ou CHOCO et sauvegarder les résultats dans les fichiers
du répertoire **`src/cop/solutions/`**.
    ```bash
    ./run_cop.sh
    ```
Pour changer le solveur utilisé ou le problème d'optimisation ou encore le temps d'exécution maximale, il suffit de modifier les variables **`SOLVER`** ,
**`PROBLEM`** et **`TIMEOUT`** dans le script **`run_cop.sh`**.


### **Résolution WCSP**  

Pour résoudre une instance du problème en utilisant le format WCSP :  

1. Exécutez la commande suivante :  
   ```bash
   python src/wcsp/wcsp.py <json_path> <wcsp_path>
   ```  
   - **`<json_path>`** : Chemin d'accès au fichier `.json` contenant l'instance du problème à modéliser et résoudre.  
   - **`<wcsp_path>`** : Chemin d'accès au dossier où l'instance traduite en format WCSP sera enregistrée, avec le nom souhaité pour le fichier.  

2. **Résultats** :  
   - Les instances traduites au format WCSP seront sauvegardées dans le répertoire **`src/wcsp/instances/`**.  
   - Les solutions et résultats générés seront enregistrés dans le répertoire **`src/wcsp/solutions/`**.  

3. **Expérimentations** :  
   Pour tester plusieurs instances et visualiser les performances :  
   - Utilisez le notebook **`wcsp_experiments.ipynb`**, qui permet de lancer des expérimentations automatisées sur différentes instances et d’analyser les résultats avec des graphiques et des statistiques.  

---

## **Références**  

- **Toulbar2** : [https://github.com/toulbar2/toulbar2](https://github.com/toulbar2/toulbar2)   
- **PyCSP3** : [https://pycsp.org/](https://pycsp.org/)

---  
