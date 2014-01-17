from PIL import Image
import numpy as np
import math
from scipy import signal


def boxfilter(n):
    assert n % 2 != 0, "Dimension must be odd"  # convention: filter center well defined
    return np.ones((n, n))/(n**2)  # sum of the filter elem. should be 1
