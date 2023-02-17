# Segmentation automatiques de lésions endométriotiques via U-NET

Ensemble de Notebook Jupyter présentant les diverses étapes nécessaires pour réaliser un apprentissage et analyser les résultats en utilisant l'architecture U-NET.

## Variable globale

Pour faire fonctionner le projet correctement, vous devez modifier la variable suivante situé dans le fichier `Modules/config.py` :

`DATA_PATH = Chemin/vers/le/dossier/contenant/les/datasets`

## Démarage

Il est nécéssaire de télécharger les datasets suivants :

- **ENID_v1.0_tracked.zip** : dataset ENID d'origine corespondant aux données mises à disposition par l'ITEC
- **DATASET.zip** : notre propre dataset où on été appliqué les étapes de pré-processing avec la répartition en trois groupes

Vous pouvez lancer le téléchargement des données et la création de l'environnement python avec la commande suivante :

```bash
chmod +x build.sh

./build.sh
```

## Tests

Une fois que votre environnement est bien configuré, vous pouvez ouvrir et exécuter les différents Notebooks mis à votre disposition dans `Notebooks/` pour visualiser nos différents travaux :

```python
1- Preprocess.ipynb
2- PreprocessFollowing.ipynb
3- Dataset_Creation.ipynb
4- Train_Model.ipynb
5- Results.ipynb
```

## Modèles

Les modèles U-NET entrainés sont disponibles `Notebooks/` :

```python
ENDOMETRIOSIS_UNET_SEG_BC_FINAL.hdf5 # Fonction de perte : Entropie coisée binaire
ENDOMETRIOSIS_UNET_SEG_JAC_FINAL.hdf5 # Fonction de perte : Score de Jaccard
```

Si vous souhaitez lancer vous-même l'apprentissage vous pouvez éxécuter la commande suivante :

```python
conda activate UNET-Endometriosis
python Scripts/train.py
```