import numpy as np
from PIL import Image
from sklearn.cluster import MiniBatchKMeans

def color_palette(path:str, num_of_colors:int):
    img = Image.open(path)
    np_img = np.array(img)
    np_img = np_img.reshape(np_img.shape[0] * np_img.shape[1], np_img.shape[2])
    normalized_colors = np_img.astype('float32') / 255
    kmeans = MiniBatchKMeans(n_clusters=num_of_colors)
    kmeans.fit(normalized_colors)
    labels = kmeans.labels_
    count = np.bincount(labels)
    cluster_centers = [tuple(i) for i in kmeans.cluster_centers_ * 255]
    color_counts = list(zip(cluster_centers, count))
    color_counts.sort(reverse=True, key=lambda x: x[1])
    rounded_colors = [(tuple(round(num, 1) for num in color), px_num) for color, px_num in color_counts]
    num_of_px = len(normalized_colors)
    return rounded_colors, num_of_px
    #fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    #ax[0].scatter(normalized_colors[:,0], normalized_colors[:,1], color=normalized_colors)
    #
    #cluster_colors = kmeans.cluster_centers_[labels]
    #ax[1].scatter(normalized_colors[:,0], normalized_colors[:,1], color=cluster_colors)
    #plt.show()

def api_color(image_file, num_color=3):
    img = Image.open(image_file)
    np_img = np.array(img)
    resolution = np_img.shape
    np_img = np_img.reshape(np_img.shape[0] * np_img.shape[1], np_img.shape[2])
    normalized_colors = np_img.astype('float32') / 255
    kmeans = MiniBatchKMeans(n_clusters=num_color)
    kmeans.fit(normalized_colors)
    labels = kmeans.labels_
    count = np.bincount(labels)
    cluster_centers = [tuple(i) for i in kmeans.cluster_centers_ * 255]
    color_counts = list(zip(cluster_centers, count))
    color_counts.sort(reverse=True, key=lambda x: x[1])
    rounded_colors = [(tuple(round(num, 1) for num in color), px_num) for color, px_num in color_counts]
    num_of_px = len(normalized_colors)
    response_dict = [{f'color{ind}': f'{data[0]}', 'pxs': f'{data[1]}'} for ind, data in enumerate(rounded_colors)]
    response_dict = {'extracted': response_dict,
                     'resolution': f'{resolution}',
                     'total_pxls': str(num_of_px),
                     'cluester_centers': str(num_color)}
    return response_dict
