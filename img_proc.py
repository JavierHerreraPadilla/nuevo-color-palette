import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def color_palette(path:str, num_of_colors:int):
    img = Image.open(path)
    np_img = np.array(img)
    print('Resolución: ', np_img.shape)
    px_colors = list()
    for row in range(np_img.shape[0]):
        for column in range(np_img.shape[1]):
            r_g_b = list()
            for plane in range(np_img.shape[2]):
                r_g_b.append(np_img[row, column, plane])
            px_colors.append(tuple(r_g_b))

    normalized_colors = np.array(px_colors) / 255
    kmeans = KMeans(n_clusters=num_of_colors)
    kmeans.fit(normalized_colors)
    labels = kmeans.labels_
    count = np.bincount(labels)
    cluster_centers = [tuple(i) for i in kmeans.cluster_centers_ * 255]
    color_counts = list(zip(cluster_centers, count))
    color_counts.sort(reverse=True, key=lambda x: x[1])
    rounded_colors = [(tuple(round(num, 1) for num in color), px_num) for color, px_num in color_counts]
    num_of_px = np_img.shape[0] * np_img.shape[1]
    return rounded_colors, num_of_px
    #fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    #ax[0].scatter(normalized_colors[:,0], normalized_colors[:,1], color=normalized_colors)
    #
    #cluster_colors = kmeans.cluster_centers_[labels]
    #ax[1].scatter(normalized_colors[:,0], normalized_colors[:,1], color=cluster_colors)
    #plt.show()
