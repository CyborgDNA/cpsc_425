from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc
from main import MakePyramid, ShowPyramid
MIN_WIDTH = 15     # min width size of the reduced images on the pyramid
THRESHOLD = 0.503  # 0.555  # mininum correlation factor to draw a red box
min_t_w = 15       # 25,20
im_path = "data/"
im_name = ["judybats.jpg","students.jpg","tree.jpg"]
im_num = 2


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
        (i, j) = template.size
        i /= 0.75 ** curr_im  # Resizes the red box
        j /= 0.75 ** curr_im

        for p in range(len(pointslist[0])):
            x = pointslist[1][p] / (0.75) ** curr_im
            y = pointslist[0][p] / (0.75) ** curr_im
            draw.rectangle([(x-i/2, y-j/2), (x+i/2, y+j/2)], outline="red")
            print x, y
        print "///"
        curr_im += 1
    del draw
    im.show()
    # im.save(im_path+"output/"+im_name[im_num], "PNG")


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
    t = template.size
    template = template.resize((min_t_w,int(template.size[1]*min_t_w/template.size[0])), Image.BICUBIC) 
    # loads the image where the match will be performed
    image = Image.open(im_path+im_name[im_num])
    # builds the pyramid list
    pyramid = MakePyramid(image, MIN_WIDTH)
    # finds the correlation between image and pyramid
    thresholded_match_list = FindTemplate(pyramid, template)
    # Marks matches on the given template
    draw_match(pyramid, template, thresholded_match_list)
