from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc

RF = 0.75  # Resize Factor


def ShowPyramid(pyramid):  # Shows the pyramid image
    pyramid_width = sum([im.size[0] for im in pyramid][:-1])  # pyramid width is equal to the sum of all witdths
    image = Image.new("L", (pyramid_width, pyramid[0].size[1]), "white")  # Creates a new image to paste the pyramid
    x_offset = 0  # Offset used to place images side by side

    for im in pyramid:
        image.paste(im, (x_offset, pyramid[0].size[1]-im.size[1]))  # Paste images side by side on the bottom
        x_offset += im.size[0]  # Increases the ofsset of the next image
    image.show()
    #image.save('data/pyramid.png','PNG')


def MakePyramid(im, minsize):
    """
    [I]:
    --------
    [O]:
    --------
    pyramid     Is a list of downsized sampled Images
    """
    pyramid = [im]  # include the original image
    size = im.size[0]

    while size >= minsize:  # As long as the sampled image still has width greater than the especified
        last = pyramid[-1]  # last sample
        (x, y) = last.size  # last sample x,y
        pyramid.append(last.resize((int(x*RF), int(y*RF)), Image.BICUBIC))  # Append to the pyramid the resized (RF) image
        size = int(last.size[0])  # Width of the last image
    return pyramid


def main():
    im = Image.open("data/template.jpg")  # loads the image
    minsize = 15  # minimum width of the last sample
    pyramid = MakePyramid(im, minsize)  # builds the pyramid list
    ShowPyramid(pyramid)  # show or save the pyramid image
