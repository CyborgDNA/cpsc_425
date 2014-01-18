from PIL import Image
import numpy as np
import math
from scipy import signal
from q3 import gauss2d
IMG_PATH = 'data/'


def im_prep(image):
    im = Image.open(IMG_PATH+image)
    im = im.convert('L')  # converts the img to bw
    im.save(IMG_PATH+"out_img1.png","PNG")  # saves the bw img to further comparison
    return np.asarray(im)  # returns the array representation


def gaussconvolve2d(image, sigma):
    im = signal.convolve2d(im_prep(image), gauss2d(sigma), 'same')  # applies the gaussian blur on the array
    im = Image.fromarray(im)  # converts it back to image representation
    im = im.convert("RGB")
    im.save(IMG_PATH+"out_img2.png","PNG")
