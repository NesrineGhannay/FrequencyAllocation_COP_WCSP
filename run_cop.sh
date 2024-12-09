#!/bin/bash

# Script qui lance la résolution des données cop

# Répertoire contenant les fichiers de données
data_dir="donnees/donnees_cop"

# Vérifie si le répertoire existe
if [ ! -d "$data_dir" ]; then
  echo "Le répertoire $data_dir n'existe pas."
  exit 1
fi

# Parcourt tous les fichiers du répertoire
for file in "$data_dir"/*; do
  if [ -f "$file" ]; then
    # echo "Traitement du fichier: $file"
    python3 src/cop/cop_freq_alloc.py "$file" --timeout 600 --problem 1 --solver ACE

  fi
done

rm *.log