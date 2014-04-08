import matplotlib.pyplot as plt
import numpy as np


def histograms(length, nbins, colors, grays):
    # Initialize color histogram
    colorhs = np.zeros((length, nbins*3), dtype=np.uint16)

    # Compute color histograms
    for i in range(length):
        v_red = colors[[i], :, :, [0]]
        v1 = np.histogram(v_red.flatten(), bins=nbins, range=(0, 255))
        v_green = colors[[i], :, :, [1]]
        v2 = np.histogram(v_green.flatten(), bins=nbins, range=(0, 255))
        v_blue = colors[[i], :, :, [2]]
        v3 = np.histogram(v_blue.flatten(), bins=nbins, range=(0, 255))
        colorhs[i] = np.hstack((v1[0], v2[0], v3[0]))

    # Initialize gray histogram
    grayhs = np.zeros((length, nbins), dtype=np.uint16)
    gbins = np.zeros(nbins+1, dtype=np.uint16)
    # Compute gray histograms
    for i in range(length):
        v_gray = grays[[i], :, :]
        grayhs[i], gbins = np.histogram(v_gray.flatten(),
                                        bins=nbins, range=(0, 255))
    # Plot Grayscale Histogram
    plt.figure(1)
    plt.plot(sum(grayhs[:, 0:nbins]))
    plt.title("Gray scale Histogram")
    plt.xlabel("bin number")
    plt.ylabel("observations")
    plt.savefig("out/histograms/grayhs.jpg")

    # Plot R,G,B Histogram
    red = sum(colorhs[:, 0:nbins])
    green = sum(colorhs[:, nbins+1:2*nbins])
    blue = sum(colorhs[:, 2*nbins+1:3*nbins])
    plt.figure(2)
    plt.title("R,G,B Histogram")
    rp, = plt.plot(red, color="red")
    gp, = plt.plot(green, color="green", linestyle="--")
    bp, = plt.plot(blue, color="blue", linestyle=":")
    plt.legend([rp, gp, bp], ["red", "green", "blue"], loc=4)
    plt.xlabel("bin number")
    plt.ylabel("observations")
    plt.savefig("out/histograms/colorhs.jpg")

    return colorhs, grayhs
