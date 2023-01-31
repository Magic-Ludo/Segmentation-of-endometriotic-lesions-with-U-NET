import numpy as np
import os
from PIL import Image
from pathlib import Path


def redimension(image, liste):
    if image.shape[0] < 360:
        rajout_lignes = np.zeros( (360 - image.shape[0], image.shape[1],3),dtype=np.uint8 )
        image = np.concatenate( (image, rajout_lignes), axis=0)
           
    else:
        image = image[:360,:,:]
        
    if image.shape[1] < 640:
        rajout_colonne = np.zeros( (image.shape[0], 640-image.shape[1],3), dtype=np.uint8 )
        image = np.concatenate( (image, rajout_colonne), axis=1)
        
    else:
        image = image[:,:640,:]

    liste.append(image)

def verifTaille(liste):
    listeTaille = []
    for i in range(len(liste)):
        listeTaille.append(liste[i].shape)

    if(len(set(listeTaille))==1):
        print("Tous les éléments de la liste ont la meme dimension")
        return 1
    
    else:
        print("Tous les éléments de la liste n'ont pas la meme dimension")
        return 0

def tailleImage(chemin, dossier):
    liste_bonnes_images = []
    src = Path(chemin)
    listFiles = [f.resolve() for f in src.glob("*.jpg")]

    for i in range(len(listFiles)):
        image = Image.open( listFiles[i] )
        image_array = np.array( image )
        if i == 0:
            liste_bonnes_images.append(image_array)
            print("la taille des images doivent etre de: ",image_array.shape)
            
        elif  image_array.shape == liste_bonnes_images[0].shape:
            liste_bonnes_images.append(image_array)

        else:
            redimension(image_array, liste_bonnes_images)
            

    if verifTaille(liste_bonnes_images):
        os.makedirs(dossier, exist_ok = True)
        nom = os.listdir(src)
        copie(nom,liste_bonnes_images, dossier) 

def copie(nom, image, dossier):
    dossier = dossier+'/'
    for i in range(len(image)):
        chemin_save = dossier+nom[i]
        im = Image.fromarray(image[i], 'RGB')
        im.save(chemin_save)
    print('copie terminer')
