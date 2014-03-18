from PIL import Image, ImageDraw
import numpy as np
import csv
import math
import random


def ReadKeys(image):
    """Input an image and its associated SIFT keypoints.

    The argument image is the image file name (without an extension).
    The image is read from the PGM format file image.pgm and the
    keypoints are read from the file image.key.

    ReadKeys returns the following 3 arguments:

    image: the image (in PIL 'RGB' format)

    keypoints: K-by-4 array, in which each row has the 4 values specifying
    a keypoint (row, column, scale, orientation).  The orientation
    is in the range [-PI, PI] radians.

    descriptors: a K-by-128 array, where each row gives a descriptor
    for one of the K keypoints.  The descriptor is a 1D array of 128
    values with unit length.
    """
    im = Image.open(image+'.pgm').convert('RGB')
    keypoints = []
    descriptors = []
    first = True
    with open(image+'.key', 'rb') as f:
        reader = csv.reader(f, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)
        descriptor = []
        for row in reader:
            if len(row) == 2:
                assert first, "Invalid keypoint file header."
                assert row[1] == 128, "Invalid keypoint descriptor length in header (should be 128)."
                count = row[0]
                first = False
            if len(row) == 4:
                keypoints.append(np.array(row))
            if len(row) == 20:
                descriptor += row
            if len(row) == 8:
                descriptor += row
                assert len(descriptor) == 128, "Keypoint descriptor length invalid (should be 128)."
                #normalize the key to unit length
                descriptor = np.array(descriptor)
                descriptor = descriptor / math.sqrt(np.sum(np.power(descriptor, 2)))
                descriptors.append(descriptor)
                descriptor = []
    assert len(keypoints) == count, "Incorrect total number of keypoints read."
    print "Number of keypoints read:", int(count)
    return [im, keypoints, descriptors]


def AppendImages(im1, im2):
    """Create a new image that appends two images side-by-side.

    The arguments, im1 and im2, are PIL images of type RGB
    """
    im1cols, im1rows = im1.size
    im2cols, im2rows = im2.size
    im3 = Image.new('RGB', (im1cols+im2cols, max(im1rows, im2rows)))
    im3.paste(im1, (0, 0))
    im3.paste(im2, (im1cols, 0))
    return im3


def DisplayMatches(im1, im2, matched_pairs):
    """Display matches on a new image with the two input images placed side by side.

    Arguments:
     im1           1st image (in PIL 'RGB' format)
     im2           2nd image (in PIL 'RGB' format)
     matched_pairs list of matching keypoints, im1 to im2

    Displays and returns a newly created image (in PIL 'RGB' format)
    """
    im3 = AppendImages(im1, im2)
    offset = im1.size[0]
    draw = ImageDraw.Draw(im3)
    for match in matched_pairs:
        draw.line((match[0][1], match[0][0], offset+match[1][1], match[1][0]), fill="red", width=2)
    im3.show()
    return im3


def match(image1, image2):
    """Input two images and their associated SIFT keypoints.
    Display lines connecting the first 5 keypoints from each image.
    Note: These 5 are not correct matches, just randomly chosen points.

    The arguments image1 and image2 are file names without file extensions.

    Returns the number of matches displayed.

    Example: match('scene','book')
    """
    im1, keypoints1, descriptors1 = ReadKeys(image1)
    im2, keypoints2, descriptors2 = ReadKeys(image2)
    #
    # REPLACE THIS CODE WITH YOUR SOLUTION (ASSIGNMENT 5, QUESTION 3)
    #

    # Threshold is between 0 and 1
    threshold = 0.93
    print "Threshold = ", threshold
    # number of times to run the RANSAC
    rounds = 100
    print "Rounds = ", rounds
    # a list of pairs of keypoints matched in both images
    matched_pairs = []
    # match keeps track of the indexes(values) of a given angle(key)
    match = {}
    # measures
    for rowim1 in xrange(len(descriptors1)):
        for rowim2 in xrange(len(descriptors2)):
            # the angle between the descriptors measures
            # the similarity between them
            angle = math.acos(np.dot(descriptors1[rowim1],
                                     descriptors2[rowim2]))
            match[angle] = (rowim1, rowim2)
        sorted_match = sorted(match)
        # best two matches
        first_nearest_neighbor = sorted_match[0]
        second_nearest_neighbor = sorted_match[1]
        # any bestmatch suficiently closer(threshold) to a second
        # minimum match is a match that we wan to keep
        if first_nearest_neighbor/second_nearest_neighbor < threshold:
            key1, key2 = match[first_nearest_neighbor]
            matched_pairs.append([keypoints1[key1], keypoints2[key2]])
        match = {}
    # calls ransac over the raw pairs
    matched_pairs = ransac(matched_pairs, keypoints1, keypoints2, rounds)
    #
    # END OF SECTION OF CODE TO REPLACE
    #
    im3 = DisplayMatches(im1, im2, matched_pairs)
    return im3


def ransac(matched_pairs, keypoints1, keypoints2, rounds):
    """
    Applies the RANSAC algorithm to the matched_pairs in order to
    reduce the amount of false positives.

    [I]:
    matched_pairs   the matched keypoints pairs calculated by match()
    keypoints1      the keypoints on the first image
    keypoints2      the keypoints on the second image
    rounds          the amount of subsets to be generated and compared
    [O]:
    best_matched_pairs  the best keypoints subset after the given rounds
    """
    # a list of keypoints of the best subset
    best_matched_pairs = []
    # subset keypoints pairs
    subset_pairs = []
    for i in range(rounds):
        # matched keypoins 1 and 2 chosen randomly from
        # the original matched_pairs
        km1, km2 = random.choice(matched_pairs)
        subset_pairs.append([km1, km2])
        # compares the random match with all the others
        for k1, k2 in matched_pairs:
            # row, columm, scale, orientation for the random pair
            _, _, sm1, om1 = km1
            _, _, sm2, om2 = km2
            # row, columm, scale, orientation for the other pairs
            _, _, s1, o1 = k1
            _, _, s2, o2 = k2
            # we will keep all the keypoints with scale and
            # orientantion close to the random match
            if(math.fabs(om1-om2-math.pi/6) < math.fabs(o1-o2)
               and math.fabs(om1-om2+math.pi/6) > math.fabs(o1-o2)
               and math.fabs(sm1-sm2)*0.5 < math.fabs(s1-s2)
               and math.fabs(sm1-sm2)*1.5 > math.fabs(s1-s2)):
                subset_pairs.append([k1, k2])
        # the largest subset is the one the we want to keep
        if(len(subset_pairs) > len(best_matched_pairs)):
            best_matched_pairs = subset_pairs
        subset_pairs = []
    return best_matched_pairs

#Test run...
# match('scene', 'book')
match('library2', 'library')
# match('scene', 'box')
