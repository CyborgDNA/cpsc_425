from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc
from main import MakePyramid
MIN_WIDTH = 15    # min width size of the reduced images on the pyramid
THRESHOLD = 0.35  # mininum correlation factor to draw a red box


def draw_match(pyramid, image, template_array_list):
    """
    Draw the red boxes corresponding to a match on the template

    [I]:
    --------
    image                 The original image
    pyramid               The resized list of the template
    template_array_list   A list of arrays(one for each template) of the
                          thresholded matches, where each array is stores
                          matching points
    """

    im = image.convert("RGB")
    draw = ImageDraw.Draw(im)

    curr_temp = 0
    pointslist = []
    for template in template_array_list:
        pointslist = np.nonzero(template)
        for p in range(len(pointslist[0])):
            x = pointslist[0][p]
            y = pointslist[1][p]
            (i, j) = pyramid[curr_temp].size
            draw.rectangle([(x, y), (x+i, y+j)], outline="red", width=2)
        curr_temp += 1
    del draw
    im.show()


def FindTemplate(pyramid, image, threshold):
    """
    Finds the correlation between image and pyramid
    [I]:
    ----------
    pyramid     A list of resized templates
    image       The given image where the match will be performed
    threshold   A constant to determine the matching areas
    [O]:
    ----------
    None
    """
    match = []
    for template in [pyramid[0]]:
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
    pyramid = MakePyramid(template, MIN_WIDTH)
    print "Templates on the pyramid:", len(pyramid)
    # finds the correlation between image and pyramid
    thresholded_match_list = FindTemplate(pyramid, image, THRESHOLD)
    # Marks matches on the given template
    draw_match(pyramid, image, thresholded_match_list)
