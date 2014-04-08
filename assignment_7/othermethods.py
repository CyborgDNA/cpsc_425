import matplotlib.pyplot as plt
import numpy as np
import math


def other(length, nbins, grayhs, grays):
    # Frame differences
    ssd = np.zeros(length/2, dtype=np.float64)
    sad = np.zeros(length/2, dtype=np.float64)
    ad = np.zeros(length/2, dtype=np.float64)
    hd = np.zeros(length/2, dtype=np.float64)

    odd = [i for i in range(length) if i % 2 != 0]
    even = range(0, length, 2)
    compare = zip(even, odd)
    i = 0

    for frame1, frame2 in compare:
        # Sum of Squared Differences
        ssd[i] = sum(sum(np.sqrt((grays[frame1, :] - grays[frame2, :])**2)))
        # Sum of Absolute Difereces
        sad[i] = sum(sum(abs(grays[frame1, :] - grays[frame2, :])))
        # Average Gray Level Differences
        ad[i] = np.average(grays[frame1, :] - grays[frame2, :])
        # Histogram Differences
        hd[i] = sum(np.sqrt((grayhs[frame1, :] - grayhs[frame2, :])**2))
        i += 1
    plot_other(ssd, sad, ad, hd)


def plot_other(ssd, sad, ad, hd):
    # SSD and SAD Plot
    plt.figure(5)
    plt.title("Differences between consecutive frames")
    ssdp, = plt.plot(ssd, color="red")
    sadp, = plt.plot(sad, color="green", linestyle="--")
    plt.legend([ssdp, sadp], ["ssd", "sad"], loc=4)
    plt.xlabel("frame pair #")
    plt.ylabel("ssd/sad value")
    plt.savefig("out/other/ssd-sad.jpg")

    # Average Gray Level Differences Plot
    plt.figure(6)
    plt.title("Average Gray Level Differences (AGLD)")
    plt.plot(ad)
    plt.xlabel("frame pair #")
    plt.ylabel("AGLD value")
    plt.savefig("out/other/ad.jpg")

    # Histogram differences
    plt.figure(7)
    plt.title("Histogram Differences")
    plt.plot(hd)
    plt.xlabel("frame pair #")
    plt.ylabel("value of SSD between histograms")
    plt.savefig("out/other/hd.jpg")

    # SAD Plot
    plt.figure(8)
    plt.title("Differences between consecutive frames")
    sadp, = plt.plot(sad, color="green", linestyle="--")
    plt.legend([sadp], ["sad"], loc=4)
    plt.xlabel("frame pair #")
    plt.ylabel("ssd/sad value")
    plt.savefig("out/other/sad.jpg")
