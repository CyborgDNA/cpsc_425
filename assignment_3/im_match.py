from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc
import sys
from pyramid import MakePyramid, ShowPyramid
im_path = "data/"
im_name = ["judybats.jpg", "students.jpg", "tree.jpg"]


def draw_match(pyramid, template, image_array_list):
    """
    Draw the red boxes corresponding to a match on the image

    [I]:
    --------
    template              The template
    pyramid               The resized list of images
    image_array_list      A list of arrays(one for each image) of the
                          thresholded matches, where each array stores
                          matching points
    """
    # Convert the image to color, so that we can put the red rectangles
    im = pyramid[0].convert("RGB")
    draw = ImageDraw.Draw(im)

    # current image
    curr_im = 0
    # list of points with correlation > threshold
    pointslist = []
    # size of the template
    (i, j) = template.size
    for image in image_array_list:
        # get the coordinates of high correlation points
        pointslist = np.nonzero(image)
        # Resizes the red box dimensions according to the image size
        i /= 0.75 ** curr_im
        j /= 0.75 ** curr_im

        # draw each rectangle centered on a correlation point
        for p in range(len(pointslist[0])):
            # resizes the points coordinates according to the size
            # of the current image
            x = pointslist[1][p] / (0.75) ** curr_im
            y = pointslist[0][p] / (0.75) ** curr_im
            draw.rectangle([(x-i/2, y-j/2), (x+i/2, y+j/2)], outline="red")
        curr_im += 1
    del draw
    im.show()
    # im.save(im_path+"output/"+im_name[im_num], "PNG")


def FindTemplate(pyramid, template, THRESHOLD):
    """
    Finds the correlation between pyramid and template
    [I]:
    ----------
    pyramid     A list of resized images
    template    The given template used to match the images on the pyramid
    THRESHOLD   Is the constant we use to discard small correlations
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


def main(im_num, MIN_TEMP_WID, THRESHOLD):
    """
    Calls the image matching pipeline
    [I]:
    --------
    im_num          Is an index to select between image sources(judybats,students,tree)
    MIN_TEMP_WID    Is the minimum template width(15)
    THRESHOLD       Is the constant we use to discard small correlations (0.503)
    """
    # loads the template
    template = Image.open(im_path+"template.jpg")
    # resize factor
    RF = int(template.size[1]*MIN_TEMP_WID/template.size[0])
    # resizes the template
    template = template.resize((MIN_TEMP_WID, RF), Image.BICUBIC)
    # loads the image where the match will be performed
    image = Image.open(im_path+im_name[im_num])
    # min width size of the reduced images on the pyramid
    MIN_WIDTH = 15
    # builds the pyramid
    pyramid = MakePyramid(image, MIN_WIDTH)
    # finds the correlation between pyramid and template
    thresholded_match_list = FindTemplate(pyramid, template, THRESHOLD)
    # draw matches on the original image
    draw_match(pyramid, template, thresholded_match_list)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
