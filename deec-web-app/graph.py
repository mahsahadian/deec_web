import matplotlib.pyplot as plt
import io
import base64

import numpy as np
import pandas as pd
w1 = np.random.uniform(0.8,1.0,(50,2))
w2 = np.random.uniform(0.0,0.2,(50,2))
X = np.concatenate((w1,w2),axis=0)


def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

def dist(a,b):
    a = np.reshape(a,(1,np.shape(a)[0],np.shape(a)[1]))
    b = np.reshape(b,(np.shape(b)[0],1,np.shape(b)[1]))

    dist = np.sqrt(np.sum(np.square(a-b), axis=2))

    a = np.reshape(a,(np.shape(a)[1],np.shape(a)[2]))
    b = np.reshape(b,(np.shape(b)[0],np.shape(b)[2]))
    return dist

def k_means(k, X):
    centroids = np.random.rand(k,np.shape(X)[1])

    error = 1
    while error != 0:
        prevcen = centroids

        cluster = np.argmin(dist(X,centroids), axis=0)

        clusters = {}
        points = {}

        for i in range(k):
            point = np.empty((0,np.shape(X)[1]))
            for j in range(np.shape(X)[0]):
                if cluster[j] == i:
                    concatenation = np.reshape(X[j,:],(1,np.shape(X)[1]))
                    point = np.concatenate((point, concatenation), axis=0)
            points = {i: point}
            clusters.update(points)

        for i in range(k):
            points = clusters[i]
            centroids[i,:] = np.mean(points, axis=0)

        error = np.linalg.norm((prevcen - centroids))

    return clusters, centroids