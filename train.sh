#!/bin/bash
bold=$(tput bold)
normal=$(tput sgr0)

DIR=/media/ludovic/Cache/TEST/

clear

cd $DIR

echo "$(tput bold)Téléchargement du Dataset en cours...$(tput sgr0)"
echo
wget -q --show-progress https://mega.nz/file/JKxxjS6A#ZZg8U0fXuDY4qYEIFlfnR6p-EpX1Pr2H-0dg8cMkoPw

echo
echo "$(tput bold)Extraction en cours...$(tput sgr0)"
unzip -o ENID_v1.0_split_60_20_20.zip | awk 'BEGIN {ORS=" "} {if(NR%10==0)print "."}'
echo
del ENID_v1.0_split_60_20_20.zip


