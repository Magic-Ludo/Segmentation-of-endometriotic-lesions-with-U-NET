#    _    _  _______  _____  _       _____   _____ 
#   | |  | ||__   __||_   _|| |     |_   _| / ____|
#   | |  | |   | |     | |  | |       | |  | (___  
#   | |  | |   | |     | |  | |       | |   \___ \ 
#   | |__| |   | |    _| |_ | |____  _| |_  ____) |
#    \____/    |_|   |_____||______||_____||_____/ 
#                                                  
#   ---------------------------------------
#   Fonctions d'utilité générale
#

import numpy as np
from PIL import Image

def progressBar(iteration, total, prefix = '', suffix = '', decimals = 0, length = 60):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = '█' * filledLength + '░' * (length-1 - filledLength)
    print(f'\r{prefix} [{bar}] {percent} % {suffix}', end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()

def fsize(num, suffix='o'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return f'{num:3.1f} {unit}{suffix}'
        num /= 1024.0
    return f'{num:.1f} Y{suffix}'

def getImgMsk(dataframe, row):
    image_path = dataframe.iloc[row][0]
    image = Image.open(image_path)
    image_array = np.array(image)

    mask_path = dataframe.iloc[row][2]
    mask = Image.open(mask_path)
    # Conversion en niveaux de gris
    mask_conv = mask.convert('L')
    mask_array = np.array(mask_conv)
    
    return image_array, mask_array

def getImgPath(image_path):
    image = Image.open(image_path)
    return np.array(image)

def getMaskPath(mask_path):
    mask = Image.open(mask_path)
    return np.array(mask)

def resize_img_mask(height_target, width_target, source_img, source_mask):
    new_img = np.zeros((height_target, width_target, 3), dtype='uint8')
    new_mask = np.zeros((height_target, width_target), dtype='uint8')

    height_src = source_img.shape[0]
    width_src = source_img.shape[1]

    decal_x = (height_target - height_src) // 2
    decal_y = (width_target - width_src) // 2

    new_img[decal_x:height_target-decal_x, decal_y:width_target-decal_y, :] = source_img
    new_mask[decal_x:height_target-decal_x, decal_y:width_target-decal_y] = source_mask

    return new_img, new_mask
        
def train_validate_test_split(df, train_percent=.6, validate_percent=.2, seed=None):
    np.random.seed(seed)
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.iloc[perm[:train_end]]
    validate = df.iloc[perm[train_end:validate_end]]
    test = df.iloc[perm[validate_end:]]
    return train, test, validate
