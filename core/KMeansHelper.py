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



def getClosestTreesIds(df, clustersNumber, plotSize):
    kmeans = KMeans(n_clusters=clustersNumber)
    centroids = getCentroidsForTrees(df, kmeans)
    labels = kmeans.predict(df)
    closest, _ = pairwise_distances_argmin_min(centroids, df)
    printKMeansChart(centroids, df, labels, clustersNumber, plotSize)
    return closest




def printKMeansChart(centroids, df, labels, clustersNumber, plotSize):
    kmeans = KMeans(n_clusters=clustersNumber)
    #centroids = getCentroidsForTrees(df, kmeans)
    colmap = {1: 'r', 2: 'g', 3: 'b', 4: 'm', 5: 'brown', 6: 'gold', 7: 'navy', 8: 'tan', 9: 'olive', 10: 'lightpink'}
    fig = plt.figure(figsize=(8, 8))
    colors = map(lambda x: colmap[x + 1], labels)
    plt.scatter(df['x'], df['y'], color=list(colors), alpha=0.5, edgecolor='k')
    for idx, centroid in enumerate(centroids):
        plt.scatter(*centroid, color=colmap[idx + 1])

    plt.xlabel('Indeks drzewa podczas iteracji', fontsize=18)
    plt.ylabel('Wartość odległości edycyjnej', fontsize=18)
    plt.xlim(0, plotSize)
    plt.ylim(0, 800)
    plt.show()

def removeAnomaliesForTree(node):
    if not node.children:
        print("There are no children for this node.")

    nodesToCheck = []
    nodesToCheck.append(node)
    treeRepresentation = []
    treeRepresentation.append(node)

    while nodesToCheck:
        currentNode = nodesToCheck.pop(0)
        for child in currentNode.children:
            if len(child.children) > 0:
                nodesToCheck.append(child)
                treeRepresentation.append(child)

    for node in treeRepresentation:
        if node in treeRepresentation:
            if len(node.children) > 0:
                for kid in node.children:
                    kid.parent = node.parent
                    node.parent.children.append(node.children)
                    node.parent.children.remove(node)
            else:
                node.parent.children.remove(node)
    return node

with open("C://Users//BKUCINSK//Documents//Docker//Magister//kmeans1days.pickle", 'rb') as rfp:
    kMeansTest = cPickle.load(rfp)

getClosestTreesIds(kMeansTest, 10, 140)
#
#
#
#with open("C://Users//BKUCINSK//Documents//Docker//Magister//exampleTree.pickle", 'rb') as et:
#    exampleTree = cPickle.load(et)
#
# cutTreeByLevel(exampleTree, 3)
#
#exampleTree = removeAnomaliesForTree(exampleTree)
#
#print(exampleTree)

#getClosestTreesIds(kMeansTest, 10, 400)