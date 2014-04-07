import matplotlib.pyplot as plt
import numpy as np
import math


def other(length, nbins, grayhs, grays):
    # Frame differences
    ssd = sad = np.zeros((length, length), dtype=np.float64)
    start = 0
    for frame1 in xrange(length):
        start += 1
        for frame2 in xrange(start, length):
            # Sum of Squared Differences
            ssd[frame1][frame2] = (sum(sum((grays[frame1, :] -
                                   grays[frame2, :])**2)))**(1/2)
            # Sum of Absolute Difereces
            sad[frame1][frame2] = (math.fabs(sum(sum(grays[frame1, :] -
                                   grays[frame2, :]))))

    plt.figure(5)
    plt.plot(ssd[0, :])
    plt.show()
    # Difference of average grayscales
    # plt.plot(davgray)

    # histogram differences
    # plt.plot(diffghists)
    pass
