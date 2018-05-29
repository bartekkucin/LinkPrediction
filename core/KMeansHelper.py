import sys
import zss
# 1

import matplotlib.pyplot as plt
import pickle as cPickle
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

def loadDatafromPickle(fileName):
    pickle_followers = open(fileName, "rb")
    df = cPickle.load(pickle_followers)
    return df

def getCentroidsForTrees(df, kmeans):
    kmeans.fit(df)
    centroids = kmeans.cluster_centers_
    return centroids



def getClosestTreesIds(df, clustersNumber):
    kmeans = KMeans(n_clusters=clustersNumber)
    #labels = kmeans.predict(df)
    centroids = getCentroidsForTrees(df, kmeans)
    closest, _ = pairwise_distances_argmin_min(centroids, df)
    return closest

    printKMeansChartt(centroids, df, labels)


def printKMeansChartt(df, clustersNumber):
    kmeans = KMeans(n_clusters=clustersNumber)
    centroids = getCentroidsForTrees(df, kmeans)
    labels = kmeans.predict(df)
    colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'brown', 6: 'gold', 7: 'navy', 8: 'tan', 9: 'olive', 10: 'lightpink'}
    fig = plt.figure(figsize=(5, 5))
    colors = map(lambda x: colmap[x + 1], labels)
    plt.scatter(df['y'], df['x'], color=list(colors), alpha=0.5, edgecolor='k')
    for idx, centroid in enumerate(centroids):
        plt.scatter(*centroid, color=colmap[idx + 1])
    plt.xlim(0, 120)
    plt.ylim(0, 2880)
    plt.show()