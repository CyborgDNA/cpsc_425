from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc


def ShowPyramid(pyramid):
    """
    Shows the pyramid image

    [I]:
    --------
    pyramid     A list of downsized images
    """
    # pyramid width is equal to the sum of all witdths
    pyramid_width = sum([im.size[0] for im in pyramid][:-1])
    # creates a canvas to paste the pyramid
    image = Image.new("L", (pyramid_width, pyramid[0].size[1]), "white")
    # offset used to place images side by side
    x_offset = 0
    for im in pyramid:
        # paste images side by side on the bottom of the canvas
        image.paste(im, (x_offset, pyramid[0].size[1]-im.size[1]))
        # increases the ofsset of the next image
        x_offset += im.size[0]
    image.show()
    image.save('data/output/pyramid.png', 'PNG')


def MakePyramid(im, minsize):
    """
    [I]:
    --------
    im          Image
    minsize     Minimum width of the last image on the pyramid

    [O]:
    --------
    pyramid     Is a list of downsized sampled Images
    """
    # Resize Factor
    RF = 0.75

    # include the original image
    pyramid = [im]
    size = im.size[0]

    # as long as the sampled image still has width greater than the especified
    while size >= minsize:
        # last sample
        last = pyramid[-1]
        # last sample x,y
        (x, y) = last.size
        # append to the pyramid the resized (RF) image
        pyramid.append(last.resize((int(x*RF), int(y*RF)), Image.BICUBIC))
        # width of the last image
        size = int(last.size[0])
    return pyramid


def main():
    # loads the image
    im = Image.open("data/judybats.jpg")
    # minimum width of the last sample
    minsize = 15
    # builds the pyramid
    pyramid = MakePyramid(im, minsize)
    # show or save the pyramid image
    ShowPyramid(pyramid)
