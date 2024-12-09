#!/bin/bash

# Script qui lance la résolution des données cop

# Répertoire contenant les fichiers de données
data_dir="donnees/donnees_cop"
SOLVER="ACE"
PROBLEM=2
TIMEOUT=600

# Vérifie si le répertoire existe
if [ ! -d "$data_dir" ]; then
  echo "Le répertoire $data_dir n'existe pas."
  exit 1
fi

# Parcourt tous les fichiers du répertoire
for file in "$data_dir"/*; do
  if [ -f "$file" ]; then
    # echo "Traitement du fichier: $file"
    python3 src/cop/cop_freq_alloc.py "$file" --timeout $TIMEOUT --problem $PROBLEM --solver "$SOLVER"

  fi
done

rm *.log