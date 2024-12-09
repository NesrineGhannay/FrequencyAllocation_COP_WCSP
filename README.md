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
    - **`scop_freq_alloc.py`** : Script principal pour modéliser et résoudre les instances COP.
  - **`vcsp/`** : Dossier où se trouve le code nécessaire pour modéliser et résoudre les instances WCSP, ainsi que les fichiers générés pour et par Toulbar2.
    - **`solutions/`** : Répertoire où se trouve le résultat de chaque résolution faites avec WCSP.
    - **`instances/`** : Répertoire contenant les instances au format WCSP générées par le script `wcsp.py` pour la résolution par Toolbar2.
    - **`wcsp.py`** : Script Python pour générer et résoudre les instances WCSP avec la bibliothèque `pytoulbar2`.

- **`run_cop.sh`**  
  Script Bash pour lancer les solveurs sur les instances COP.

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

---  
