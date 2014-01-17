from PIL import Image
import numpy as np
import math
from scipy import signal
from q2 import gauss1d


def gauss2d(sigma):
    v = gauss1d(sigma)[np.newaxis]  # Converts the array from 1D to 2D
    return signal.convolve2d(v,v.T)  # Convolves 2D_v with its transpose
