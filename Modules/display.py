#    _____  _____   _____  _____   _             __     __
#   |  __ \|_   _| / ____||  __ \ | |         /\ \ \   / /
#   | |  | | | |  | (___  | |__) || |        /  \ \ \_/ / 
#   | |  | | | |   \___ \ |  ___/ | |       / /\ \ \   /  
#   | |__| |_| |_  ____) || |     | |____  / ____ \ | |   
#   |_____/|_____||_____/ |_|     |______|/_/    \_\|_|   
#
#   ---------------------------------------
#   Fonctions d'affichage
#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from skimage import exposure, img_as_float


def plot3(image_array, mask_array):
    gs = gridspec.GridSpec(2, 2)

    fig = plt.figure(figsize=(20, 10))

    ax1 = fig.add_subplot(gs[0, 0]) # row 0, col 0
    ax1.imshow(image_array)
    ax1.axis('off')
    ax1.set_title("Image laparoscopique")

    ax2 = fig.add_subplot(gs[0, 1]) # row 0, col 1
    ax2.imshow(mask_array, interpolation=None)
    ax2.axis('off')
    ax2.set_title("Masque")

    ax3 = fig.add_subplot(gs[1, :]) # row 1, span all columns
    ax3.imshow(image_array)
    masked_array = np.ma.masked_where(mask_array == 0, mask_array)
    ax3.imshow(masked_array, interpolation=None, cmap='cool')
    ax3.axis('off')
    ax3.set_title("Superposition des deux")

def plot_pred(image_array, mask_array, pred_mask_array):
    plt.figure(figsize=(20, 15))
    plt.subplot(231)
    plt.title('Image de test')
    plt.imshow(image_array)
    plt.axis('off')
    plt.subplot(232)
    plt.title('Masque originel')
    plt.imshow(mask_array, cmap='cool')
    plt.axis('off')
    plt.subplot(233)
    plt.title('Masque prédit')
    plt.imshow(pred_mask_array, cmap='cool')
    plt.axis('off')
    plt.show()

def plot_img_and_hist(image, axes, bins=256):
    
    image = img_as_float(image)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    ax_img.imshow(image)
    ax_img.set_axis_off()

    # Partie histogramme
    ax_hist.hist(image.ravel(), bins=bins, histtype='step')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Intensité des pixels')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Distribution cumulée
    img_cdf, bins = exposure.cumulative_distribution(image, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf