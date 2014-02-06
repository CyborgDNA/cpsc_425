from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc
from main import MakePyramid
MIN_WIDTH = 15    # min width size of the reduced images on the pyramid
THRESHOLD = 0.5  # mininum correlation factor to draw a red box


def draw_match(pyramid, template, image_array_list):
    """
    Draw the red boxes corresponding to a match on the template

    [I]:
    --------
    template              The template
    pyramid               The resized list of images
    image_array_list      A list of arrays(one for each image) of the
                          thresholded matches, where each array stores
                          matching points
    """

    im = pyramid[0].convert("RGB")
    draw = ImageDraw.Draw(im)

    curr_im = 0
    pointslist = []
    for image in image_array_list:
        pointslist = np.nonzero(image)
        print pyramid[curr_im].size
        print "###", curr_im
        for p in range(len(pointslist[0])):
            x = pointslist[1][p] / (0.75) ** curr_im
            y = pointslist[0][p] / (0.75) ** curr_im
            (i, j) = template.size
            draw.rectangle([(x, y), (x+i * 0.75 ** curr_im, y+j * 0.75 ** curr_im)], outline="red")
            # draw.point((x, y), "red")
            print x, y
        print "///"
        curr_im += 1
    del draw
    im.show()


def FindTemplate(pyramid, template):
    """
    Finds the correlation between image and pyramid
    [I]:
    ----------
    pyramid     A list of resized templates
    image       The given image where the match will be performed
    THRESHOLD   A constant to determine the matching areas
    [O]:
    ----------
    None
    """
    match = []
    for image in pyramid:
        match.append(ncc.normxcorr2D(image, template))
    thresholded_match_list = []
    for m in match:
        thresholded_match_list.append(np.where(m >= THRESHOLD, 1, 0))
    return thresholded_match_list


def main():
    """
    Calls the image matching pipeline
    """

    # loads the template
    template = Image.open("data/template.jpg")
    # loads the image where the match will be performed
    image = Image.open("data/judybats.jpg")
    # builds the pyramid list
    pyramid = MakePyramid(image, MIN_WIDTH)
    # finds the correlation between image and pyramid
    thresholded_match_list = FindTemplate(pyramid, template)
    # Marks matches on the given template
    draw_match(pyramid, template, thresholded_match_list)
