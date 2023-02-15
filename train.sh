#!/bin/bash
bold=$(tput bold)
normal=$(tput sgr0)

DIR=/media/ludovic/Cache/TEST/

clear

cd $DIR

while true; do
    read -p "Voulezvous télécharger le Dataset orignel ? [Y/N]" yn
    case $yn in
        [Yy]* ) echo "cool"; break;;
        [Nn]* ) exit;;
        * ) echo "Merci de répondre par Y ou N.";;
    esac
done

echo "$(tput bold)Téléchargement du Dataset en cours...$(tput sgr0)"
echo
#wget -q --show-progress https://magic-solutions.fr/DATASET.zip

echo
echo "$(tput bold)Extraction en cours...$(tput sgr0)"
unzip -o DATASET.zip | awk 'BEGIN {ORS=" "} {if(NR%100==0)print "."}'
echo
rm DATASET.zip

echo "$(tput bold)Créaton d'un environement Python...$(tput sgr0)"
echo
conda env create --file UNET-Endometriosis.yml --python=3.9.0


