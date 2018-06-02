# coding: utf-8

import sys
import zss
import os
# 1
import pandas.core.indexes
import pandas as pd
import core.TagNode as TagNode
import core.EditDistance as EditDistance
import core.DepthSerializer as depthSerializer
import networkx as nx
import core.KMeansHelper as kms
import matplotlib.pyplot as plt
import pickle as cPickle
import numpy as np
import gc
import time
import copy
import jsonpickle
from multiprocessing import Pool, Value, Manager

sys.modules['pandas.indexes'] = pandas.core.indexes


def cacheUsersWithTheirFollowers2(pfo):
    start = time.time()

    distinctUsers = (pfo.drop(['user2'], axis=1)).drop_duplicates()
    distinctUsers['followers'] = ""
    distinctUsers.index = range(len(distinctUsers.index))

    for index, row in distinctUsers.iterrows():

        currentUser = row['user1']
        usersSelected = pfo.loc[pfo['user1'] == int(currentUser)]['user2']

        distinctUsers.set_value(index, 'followers', usersSelected.values)
        print("Added an user: {0} to dictionary. Remains: {1}".format(currentUser, len(distinctUsers.index) - index))
        if (len(distinctUsers.index) - index) % 1000 == 0:
            print("Jak bardzo jestem w dupie na kazdy 1000 iteracji: {0}".format(time.time() - start))
    distinctUsers.to_pickle("C://Users//BKUCINSK//Documents//Docker//Magister//followersOptimized.pickle")

    return distinctUsers



def getFollowersListByUser(user):
    start = time.time()
    usersSelected = pfo.loc[pfo['user1'] == int(user)]['followers']
    end = time.time()
    print(end-start)
    if(len(usersSelected.values) > 0):
        return usersSelected.values.tolist()[0]
    else:
        return usersSelected.values

pickle_tags = open("C://Users//BKUCINSK//Documents//Docker//Magister//tag.pickle", "rb")
gc.disable()
emp = cPickle.load(pickle_tags)
pickle_tags.close()

#TODO: Sprawdzic usera '555053'

pickle_followers = open("C://Users//BKUCINSK//Documents//Docker//Magister///followersOptimized.pickle", "rb")
pfo = cPickle.load(pickle_followers)
pickle_followers.close()
gc.enable()

def depth(d, level=1):
    if not d or not d.children:
        return level
    return max(depth(d.children[k], level + 1) for k in range(len(d.children)))


def transformDFObjects2Node(sortedByTag):
    nodesList = []
    nodesDistinctList = []
    for index, row in sortedByTag.iterrows():
        tag = row['tag']
        user = row['user']
        time = row['ts']
        n = TagNode.make_node(tag, user, time)

        if n not in nodesDistinctList:
            nodesList.append(n)
            nodesDistinctList.append(n)

    return nodesList

def buildTree(nodes):

    treesFilteredList = set();
    for i in range(0, len(nodes)):
        nodesReadyToPick = []
        distinctNodes = set()

        tempNodesList = copy.deepcopy(nodes)
        nodesReadyToPick.append(tempNodesList[i])

        while nodesReadyToPick:
            currentNode = nodesReadyToPick.pop(0)
            users = getFollowersListByUser(currentNode.user)
            print("{0}. {1} in work line / {2} users.".format(i, currentNode.user, len(nodes)))
            for j in range(tempNodesList.index(currentNode) + 1, len(tempNodesList) - 1):
                if tempNodesList[j] not in distinctNodes and int(tempNodesList[j].user) in users and \
                                int(tempNodesList[j].ts) > int(currentNode.ts):

                    currentNode.add_child(tempNodesList[j])
                    nodesReadyToPick.append(tempNodesList[j])
                    distinctNodes.add(tempNodesList[j])

        for k in range(0, len(tempNodesList)):
            if depth(tempNodesList[k]) >= 3:
                tempNodesList[k] = calculateLevelsForTree(tempNodesList[k])
                treesFilteredList.add(tempNodesList[k])

    highestDepthTree = printTreeWithHighestDepth(treesFilteredList)

    cPickle.dump(highestDepthTree, open("C://Users//BKUCINSK//Documents//Docker//Magister//exampleTree.pickle", "wb"),
                 cPickle.HIGHEST_PROTOCOL)

    return treesFilteredList

def countDistancesBetweenNodesInTrees(treesFilteredList):
    for i in range(0, len(treesFilteredList)):
        currentTreeRoot = treesFilteredList[i]
        recursiveIterateChildren(currentTreeRoot)

def recursiveIterateChildren(node):
    for child in node.children:
        child.set_distance(int(child.ts) - int(node.ts))
        if child.children:
            for childd in child.children:
                recursiveIterateChildren(childd)



def countTreesByDepth(nodesDepthList):
    nodesDepthList.sort();
    depthCount = 0;
    depthSerializerList = list();
    for i in range(0, len(nodesDepthList)):
        currentDepthValue = nodesDepthList[i];

        if i < (len(nodesDepthList) - 1) and currentDepthValue != nodesDepthList[i + 1]:
            depthSerializerList.append(depthSerializer.make_depthSerializer(currentDepthValue, depthCount));
            if i + 1 == (len(nodesDepthList) - 1):
                depthSerializerList.append(depthSerializer.make_depthSerializer(nodesDepthList[i] + 1, 1));
                break;
            depthCount = 0;
        else:
            depthCount += 1;
    print(depthSerializerList)


def printTreeWithHighestDepth(nodes):
    highestDepthValue = 0
    highestDepthValueNode = {}
    for node in nodes:
        depthValue = depth(node)
        if depthValue > highestDepthValue:
            highestDepthValue = depthValue
            highestDepthValueNode = node
    print(highestDepthValueNode)

    return highestDepthValueNode

def calculateLevelsForTree(node):
    if not node.children:
        print("There are no children for this node.")

    nodesToCheck = []
    nodesToCheck.append(node)

    while nodesToCheck:
        currentNode = nodesToCheck.pop(0)
        if currentNode.parent and currentNode.level == currentNode.parent.level:
            currentNode.set_level(currentNode.parent.level + 1)

        for child in currentNode.children:
            child.set_level(currentNode.level + 1)
            child.parent.level = currentNode.level
            if len(child.children) > 0:
                nodesToCheck.append(child)

    return node


def printTree(pfo, nodes):

    G = nx.DiGraph()

    #initialize root
    root = nodes[0]
    G.add_node(str(root.ts), tag=root.tag)

    for i in range(1, len(nodes)):
        user = nodes[i].user
        G.add_node(str(nodes[i].ts), tag=nodes[i].tag)
        if user != root.user:
            users = getFollowersListByUser(user, pfo)
            for x in users:
                print(x)
                for nodee in nodes:
                    if nodee.user == str(x):
                        G.add_edge(nodes[i - 1].ts, nodee.ts)

    G.nodes(data=True)

    # write dot file to use with graphviz
    # run "dot -Tpng test.dot >test.png"
    #nx.nx_pydot.write_dot(G, 'test.dot')

    # same layout using matplotlib with no labels
    plt.title(str(root.tag))
    pos = nx.spring_layout(G)
    nx.draw_networkx_edges(G, pos, with_labels=True, arrows=True, width=0.5, alpha=0.5)
    plt.savefig('nx_test.png')

    plt.figure(figsize=(18,18))
    plt.show()


def buildPrototypes(tag):
    sortedByTag = emp.loc[emp['tag'].str.strip() == tag]
    nodesList = transformDFObjects2Node(sortedByTag)
    nodesList.sort(key=lambda x: x.ts, reverse=False)
    treeFilteredList = list(buildTree(nodesList))
    kmeansDataFrame = pd.DataFrame(columns=['x', 'y'])
    temporaryTreeList = []
    for j in range(0, len(treeFilteredList)):
        for i in range(j, len(treeFilteredList) - 1):
            dist = zss.simple_distance(
                treeFilteredList[j], treeFilteredList[i + 1], TagNode.Node.get_children, TagNode.Node.get_label,
                EditDistance.weird_dist)
            temporaryTreeList.append(treeFilteredList[i + 1])

            tempDF = pd.DataFrame([[i + 1, int(dist)]], columns=['x', 'y'])
            kmeansDataFrame = kmeansDataFrame.append(tempDF, ignore_index=True)
            print(dist)
    temporaryTreeList = np.array(temporaryTreeList)
    closestTrees = kms.getClosestTreesIds(kmeansDataFrame, 10, len(temporaryTreeList))
    prototypes = temporaryTreeList[closestTrees]

    protList = []
    if os.path.exists("C://Users//BKUCINSK//Documents//Docker//Magister//prototypes.pickle"):
        with open("C://Users//BKUCINSK//Documents//Docker//Magister//prototypes.pickle", 'rb') as rfp:
            protList = cPickle.load(rfp)

    protList.append(prototypes)

    cPickle.dump(protList, open("C://Users//BKUCINSK//Documents//Docker//Magister//prototypes.pickle", "wb"),
                 cPickle.HIGHEST_PROTOCOL)
    kmeansDataFrame.to_pickle("C://Users//BKUCINSK//Documents//Docker//Magister//kmeansTest.pickle")


if __name__ == '__main__':

    df = emp.groupby(['tag', 'user']).size().reset_index(name='counts')

    df2 = df.groupby(['tag']).size().reset_index(name='usersPerTagCount')

    dfTagsCount = df2.loc[df2['usersPerTagCount'] >= 500]

    tagsWithCountedUsers = pd.merge(emp, dfTagsCount, on='tag', how='inner')
    sortedByTS = tagsWithCountedUsers.sort_values(by=['ts'], ascending=True)


    dupa = sortedByTS.groupby(['tag']).size().reset_index(name='usersPerTagCount')
    print(dupa)

    del df
    del df2
    del dfTagsCount
    del tagsWithCountedUsers
    del sortedByTS
    del pickle_tags
    del pickle_followers


    gc.collect()

    tagsToCompute = []
    for i in range (1, 100):
        selectedTag = dupa.iloc[i]['tag']
        tagsToCompute.append(selectedTag)
    #buildPrototypes(selectedTag)

    try:

        pool = Pool(2)
        pool.map(buildPrototypes, tagsToCompute)

        del df
        del df2
        del dfTagsCount
        del tagsWithCountedUsers
        del sortedByTS
        del pickle_tags
        del pickle_followers

        buildPrototypes(tagsToCompute)
    finally:
        pool.close()
        pool.join()

