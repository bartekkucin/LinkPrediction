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
import time
import copy


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
    distinctUsers.to_pickle("C://Users//BKUCINSK//Documents//Docker//Magister//followersOptimized.pickle")

    return distinctUsers



def getFollowersListByUser(user):
    usersSelected = pfo.loc[pfo['user1'] == int(user)]['followers']
    if(len(usersSelected.values) > 0):
        return usersSelected.values.tolist()[0]
    else:
        return usersSelected.values

#gc.disable()
pickle_tags = open("C://Users//BKUCINSK//Documents//Docker//Magister//valuableNodes.pickle", "rb")
emp = cPickle.load(pickle_tags)
pickle_tags.close()

#TODO: Sprawdzic usera '555053'

pickle_followers = open("C://Users//BKUCINSK//Documents//Docker//Magister///followersOptimized.pickle", "rb")
pfo = cPickle.load(pickle_followers)
pickle_followers.close()
#gc.enable()

def depth(d, level=1):
    if not d or not d.children:
        return level
    return max(depth(d.children[k], level + 1) for k in range(len(d.children)))

def getTreesByDepth(d, desiredLevel, level=1):
    if not d or not d.children:
        return level
    if level == desiredLevel:
        return level
    return max(depth(d.children[k], level + 1) for k in range(len(d.children)))


def transformDFObjects2Node(sortedByTag):
    nodesList = list()
    usersDistinctList = set()
    for index, row in sortedByTag.iterrows():
        tag = row['tag']
        user = row['user']
        time = row['ts']
        n = TagNode.make_node(tag, user, time)
        if n.user not in usersDistinctList:
            nodesList.append(n)
            usersDistinctList.add(n.user)

    return nodesList

def isAlreadyUsedToCreateATree(node, distinctNodes):
    for x in distinctNodes:
        if node.user == x.user and node.tag == x.tag and node.ts == x.ts:
            return True
    return False

def buildTree(nodes):

    distinctNodes = set()
    treesFilteredList = set()

    for index, node in enumerate(nodes):
        if isAlreadyUsedToCreateATree(node, distinctNodes):
            print("Gotcha")
        else:
            print("Remains trees to build: {0}".format(len(nodes) - index))
            nodesReadyToPick = []
            #distinctNodes = set()

            tempNodesList = copy.deepcopy(nodes)
            nodesReadyToPick.append(tempNodesList[index])

            while nodesReadyToPick:
                currentNode = nodesReadyToPick.pop(0)
                users = getFollowersListByUser(currentNode.user)
                #print("{0}. {1} in work line / {2} users.".format(i, currentNode.user, len(nodes)))

                for k, smallNode in enumerate(tempNodesList, start = tempNodesList.index(currentNode) + 1):

                    if smallNode not in distinctNodes and int(smallNode.user) in users and \
                                    int(smallNode.ts) > int(currentNode.ts):

                        currentNode.add_child(smallNode)
                        nodesReadyToPick.append(smallNode)
                        distinctNodes.add(smallNode)



            for tree in tempNodesList:
                if depth(tree) >= 4:
                    tree = calculateLevelsForTree(tree)
                    treesFilteredList.add(tree)

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

    nodes = transformDFObjects2Node(sortedByTag)
    if(len(nodes) < 10000):
        nodes.sort(key=lambda x: x.ts, reverse=False)
        filteredForest = list(buildTree(nodes))
    else:
        return

    treeFilteredLists = [filteredForest[x:x + 200] for x in range(0, len(filteredForest), 200)]

    for treeFilteredList in treeFilteredLists:
        kmeansDataFrame = pd.DataFrame(columns=['x', 'y'])
        temporaryTreeList = list()
        for j, tree1 in enumerate(treeFilteredList):
            print("Remains: {0}".format(len(treeFilteredList) - j))
            for i, tree2 in enumerate(treeFilteredList, start = j + 1):
                dist = zss.simple_distance(
                    tree1, tree2, TagNode.Node.get_children, TagNode.Node.get_label,
                    EditDistance.weird_dist)
                temporaryTreeList.append(tree2)

                tempDF = pd.DataFrame([[i, int(dist)]], columns=['x', 'y'])
                kmeansDataFrame = kmeansDataFrame.append(tempDF, ignore_index=True)
        temporaryTreeList = np.array(temporaryTreeList)
        if( len(treeFilteredList) >= 10):
            closestTrees = kms.getClosestTreesIds(kmeansDataFrame, 10, len(treeFilteredList) + 50)
            prototypes = temporaryTreeList[closestTrees]

            protList = []
            if os.path.exists("C://Users//BKUCINSK//Documents//Docker//Magister//prototypes.pickle"):
                with open("C://Users//BKUCINSK//Documents//Docker//Magister//prototypes.pickle", 'rb') as rfp:
                    protList = cPickle.load(rfp)

            protList.append(prototypes)

            cPickle.dump(protList, open("C://Users//BKUCINSK//Documents//Docker//Magister//prototypes.pickle", "wb"),
                         cPickle.HIGHEST_PROTOCOL)
            #kmeansDataFrame.to_pickle("C://Users//BKUCINSK//Documents//Docker//Magister//kmeansTest.pickle")


if __name__ == '__main__':


    st = open("C://Users//BKUCINSK//Documents//Docker//Magister//selectedValuableTags.pickle", "rb")
    selectedTags = cPickle.load(st)
    st.close()

    #gc.collect()

    tagsToCompute = []
    #pool = Pool(2)

# Dodaj 3
    #for i in range (364, 400):

    selectedTag = selectedTags.iloc[16]['tag']
    #print("Now building for tag: {0}/{1}".format(selectedTag, i))
        # i = Process(target=buildPrototypes, args=(selectedTag,))
    # i.start()
    # i.join()
    #     tagsToCompute.append(selectedTag)
    # pool.apply_async(buildPrototypes, (selectedTag, ))
    buildPrototypes(selectedTag)

    # pool = ThreadPool(5)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    # pool.map(buildPrototypes, tagsToCompute)
    # pool.wait_completion()
