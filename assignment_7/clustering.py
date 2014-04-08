import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
from PIL import Image, ImageDraw


def find_indices(colorhs, centres):
    """
    Does the exact same thing as vq(colorhs, centres)[0]. That is,
    return the indices of each point in the colourhs that indicates
    which cluster it belongs to.

    [I]:
    colorhs     R,G,B histograms of all frames.
    centres     centres defined by k-means.

    [O]:
    indices     indices defining which cluster the frame belongs to.
    """

    indices = np.zeros(colorhs.shape[0], dtype=np.uint8)
    i = 0

    for hs in colorhs:
        # Past Euclidian distance
        past_ed = float("inf")
        for cluster in range(centres.shape[0]):
            # Current Euclidian distance
            curr_ed = (sum((hs - centres[cluster, :]) ** 2)) ** 1/2
            # A frame belongs to the cluster with the minimum ed value.
            if curr_ed <= past_ed:
                past_ed = curr_ed
                indices[i] = cluster
        i += 1
    return indices


def clustering(length, nbins, colorhs, grayhs, colors, grays):
    # Set specifications for using kmeans
    clusters = 4
    trials = 10
    ndim = nbins*3
    cs = np.zeros((clusters, ndim))  # cluster centres
    idxs_color = np.zeros(length)

    colorhs = whiten(colorhs)

    # Kmeans on Color
    for dim in range(ndim):
        cs[:, dim], distortion = kmeans(colorhs[:, dim], clusters, iter=trials)

    idxs_color = find_indices(colorhs, cs)

    # Kmeans on Gray
    cs = np.zeros((clusters, ndim))  # cluster centres
    idxs_gray = np.zeros(length)

    cs, distortion = kmeans(grayhs, clusters, iter=trials)
    idxs_gray = find_indices(grayhs, cs)

    plot_cluster(length, clusters, idxs_color, idxs_gray, colors, grays)


def plot_cluster(length, clusters, idxs_color, idxs_gray, colors, grays):
    # Kmeans on Color Plot
    plt.figure(3)
    plt.bar(range(length), idxs_color, width=1)
    plt.title("K-means clustering(color)")
    plt.xlabel("frame number")
    plt.ylabel("assigned cluster")
    plt.savefig("out/histograms/kmeans(color).jpg")

    # Save the clustered pics in /out/clusters_col
    for choice in range(clusters):
        for i in range(length):
            if (int(idxs_color[i]) == choice):
                out_cluster_col = Image.fromarray(colors[i])
                out_cluster_col.save("out/clusters_col/choice" +
                                     str(choice)+"Frame"+str(i)+".png")

    # Kmeans on grays Plot
    plt.figure(4)
    plt.bar(range(length), idxs_gray, width=1)
    plt.title("K-means clustering(gray)")
    plt.xlabel("frame number")
    plt.ylabel("assigned cluster")
    plt.savefig("out/histograms/kmeans(gray).jpg")

    # Save the clustered pics in /out/clusters_col
    for choice in range(clusters):
        for i in range(length):
            if (int(idxs_gray[i]) == choice):
                out_cluster_gray = Image.fromarray(grays[i])
                out_cluster_gray.save("out/clusters_gray/choice" +
                                      str(choice)+"Frame"+str(i)+".png")
