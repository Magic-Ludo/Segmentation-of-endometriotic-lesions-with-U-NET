##### CE FICHIER TOUTES LES FONCTION QUE L'ON A CREER ######
import numpy as np

def redimension(image, liste):
    image_final = image
    #si les lignes sont inferieur a 360 on rajoute des 0
    if len(image[:,0,0]) < 360:
        rajout_lignes = np.zeros( (360 - len(image[:,0,0]), len(image[0,:,0]),3) )
        image_final = np.concatenate( (image, rajout_lignes), axis=0)
           
    #si les lignes sont supp a 360 on retir des lignes
    if len(image[:,0,0]) > 360:
        image_final = image[:360,:,:]
        
    #si les colonnes sont inferieur a 640 on rajoute des 0
    if len(image[0,:,0]) < 640:
        rajout_colonne = np.zeros( (len(image_final[:,0]), 640-len(image_final[0,:,0]),3) )
        image_final = np.concatenate( (image_final, rajout_colonne), axis=1)
        
    #si les colonne sont supp a 640 on retir des colonnes
    if len(image[0,:,0]) > 640:
        image_final = image_final[:,:640,:]

    liste.append(image_final)

def verifTaille(liste):
    listeTaille = []
    for i in range(len(liste)):
        listeTaille.append(liste[i].shape)

    if(len(set(listeTaille))==1):
        print("Tous les éléments de la liste ont la meme dimension")
    else:
        print("Tous les éléments de la liste n'ont pas la meme dimension")
    
def tailleImage(chemin):
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

        elif image_array.shape != liste_bonnes_images[0].shape:
            redimension(image_array, liste_bonnes_images)


    verifTaille(liste_bonnes_images)
        
