#!/bin/bash
bold=$(tput bold)
normal=$(tput sgr0)

DIR=/media/ludovic/Cache/TEST/

clear

cd $DIR

echo "$(tput bold)Téléchargement du Dataset en cours...$(tput sgr0)"
echo
#wget -q --show-progress https://magic-solutions.fr/DATASET.zip

echo
echo "$(tput bold)Extraction en cours...$(tput sgr0)"
unzip -o DATASET.zip | awk 'BEGIN {ORS=" "} {if(NR%100==0)print "."}'
echo
rm DATASET.zip

