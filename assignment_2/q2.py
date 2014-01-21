from PIL import Image
import numpy as np
from math import pi, sqrt
from scipy import signal


def gauss1d(sigma):
    assert sigma > 0, "Sigma greather than zero"
    factor = round(6*sigma)
    array_length = factor if factor % 2 else factor+1  # the filter must have a odd center

    # (1/(2*pi*sigma**2))*exp(- x^2 / (2*sigma^2))
    x = np.arange((-array_length+1)/2, (array_length+1)/2, 1)  # generates the distance from center array
    x = (1/(sqrt(2*pi)*sigma))*np.exp(-np.square(x)/(2*sigma**2))  # calculates the gaussian function to each element
    return x/sum(x)  # return the normalized array
