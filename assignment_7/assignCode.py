from PIL import Image, ImageDraw
import numpy as np
from histograms import histograms
from clustering import clustering
from othermethods import other


def main():
    f = "colours"
    length = 151
    r = 90
    c = 120
    nbins = 10
    colors = np.zeros((length, r, c, 3), dtype=np.uint8)
    grays = np.zeros((length, r, c), dtype=np.uint8)

    # Read the images and store them in color and grayscale formats
    for i in range(length):
        im = Image.open(f+"/dwc"+str(i+1).zfill(3)+".png").convert('RGB')
        colors[i] = np.asarray(im, dtype=np.uint8)
        grays[i] = np.asarray(im.convert('L'))

    # Save the color and grayscale images
    # for i in range(length):
    #     out_col = Image.fromarray(colors[i])
    #     out_gray = Image.fromarray(grays[i])
    #     out_col.save("out/col_im/dwc_col"+str(i+1).zfill(3)+".png")
    #     out_gray.save("out/gray_im/dwc_gray"+str(i+1).zfill(3)+".png")

    # Draw histograms
    colorhs, grayhs = histograms(length, nbins, colors, grays)

    # Kmeans
    # clustering(length, nbins, colorhs, grayhs, colors, grays)

    # Other Methods
    other(length, nbins, grayhs, grays)

if __name__ == '__main__':
    main()
