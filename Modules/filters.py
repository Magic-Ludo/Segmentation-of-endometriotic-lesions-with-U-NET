#    ______  _____  _    _______  ______  _____    _____ 
#   |  ____||_   _|| |  |__   __||  ____||  __ \  / ____|
#   | |__     | |  | |     | |   | |__   | |__) || (___  
#   |  __|    | |  | |     | |   |  __|  |  _  /  \___ \ 
#   | |      _| |_ | |____ | |   | |____ | | \ \  ____) |
#   |_|     |_____||______||_|   |______||_|  \_\|_____/ 
# 
#   ---------------------------------------
#   Fonctions de filtre
#

import numpy as np
from skimage import exposure, filters
from scipy import ndimage
import cv2

#   Filtre gaussien (denoise)
def gaussian_filter(image, sigma):
    return ndimage.gaussian_filter(image, sigma)

#   Filter median (denoise)
def median_filter(image, size):
    return ndimage.median_filter(image, size)

#   Accentuation
def sharpening(image, sigma, alpha):
    def unsharp(image, sigma, alpha):
        # Median filtering
        image_mf = median_filter(image, sigma)

        # Calculate the Laplacian
        lap = cv2.Laplacian(image_mf,cv2.CV_64F)

        # Calculate the sharpened image
        sharp = image-alpha*lap

        sharp[sharp>255] = 255
        sharp[sharp<0] = 0
        
        return sharp
    
    sharped_img = np.zeros_like(image)
    for i in range(3):
        sharped_img[:,:,i] = unsharp(image[:,:,i], sigma, alpha)
    
    return sharped_img

#   Egalisation d'histogramme (auto contraste)
def hist_equal(image):
    return exposure.equalize_hist(image)

#   Etirement d'histogramme
def hist_stretching(image):
    p3, p95 = np.percentile(image, (5, 92))
    return exposure.rescale_intensity(image, in_range=(p3, p95))

#   Ouverture morphologique
def remove_noise_open(image, open):
    open_img = ndimage.binary_opening(image, iterations=open)
    return ndimage.binary_propagation(open_img, mask=image)

#   Fermeture morphologique
def remove_noise_close(image, close):
    eroded_img = ndimage.binary_erosion(image, iterations=close)
    return ndimage.binary_propagation(eroded_img, mask=image)

#   Filtre de Sobel (détéction de contours)
def sobel(image):
    sx = ndimage.sobel(image, axis=0, mode='reflect')
    sy = ndimage.sobel(image, axis=1, mode='reflect')
    sob = np.hypot(sx, sy)
    return sob

#   Seuillage global
def global_thresholding(image):
    global_thresh = filters.threshold_otsu(image)
    return image > global_thresh

#   Seuillage local
def local_thresholding(image, size):
    local_thresh = filters.threshold_local(image, size, offset=10)
    return image > local_thresh