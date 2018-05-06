# coding: utf-8

import sys
# 1
import pandas.core.indexes
import pandas as pd
import core.Node as node
import core.DepthSerializer as depthSerializer
import networkx as nx
import pydot
import graphviz
import matplotlib.pyplot as plt
import pickle as cPickle
import gc
sys.modules['pandas.indexes'] = pandas.core.indexes

pickle_tags = open("C://Users//BKUCINSK//Documents//Docker//Magister//tag.pickle", "rb")
gc.disable()
emp = cPickle.load(pickle_tags)
pickle_tags.close()

pickle_followers = open("C://Users//BKUCINSK//Documents//Docker//Magister///follower.pickle", "rb")
pfo = cPickle.load(pickle_followers)
pickle_followers.close()
gc.enable()

treesList = []

def getFollowersListByUser(user, dfx):
    usersSelected = dfx.loc[dfx['user1'] == int(user)]
    usersList = []
    for index, row in usersSelected.iterrows():
        user = row['user2']
        usersList.append(user)
    return usersList

def depth(d, level=1):
    if not d or not d.children:
        return level
    return max(depth(d.children[k], level + 1) for k in range(len(d.children)))


def transformDFObjects2Node(sortedByTag):
    nodesList = []
    nodesUsersList = []
    for index, row in sortedByTag.iterrows():
        tag = row['tag']
        user = row['user']
        time = row['ts']
        n = node.make_node(tag, user, time)

        if n.user not in nodesUsersList:
            nodesList.append(n)
            nodesUsersList.append(n.user)

    return nodesList

def buildTree(nodes):
    #create root

    for i in range(0, len(nodes)):
        user = nodes[i].user
        users = getFollowersListByUser(user, pfo)
        print("{0}. {1} in work line / {2} users.".format(i, nodes[i].user, len(nodes)))
        for x in users:
            #if x not in distinctNodesUsers:
                for nodee in nodes:
                    if nodee.user == str(x) and int(nodee.ts) > int(nodes[i].ts):
                        nodes[i].add_child(nodee)
                        #distinctNodesUsers.append(x)

    nodesDepthList = list();
    #Grouping by Tree's depth
    for i in range(0, len(nodes)):
        nodesDepthList.append(depth(nodes[i]))

    printTreeWithHighestDepth(nodes)

    countTreesByDepth(nodesDepthList)


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
    highestDepthValueNodeNumber = 0
    for i in range(0, len(nodes)):
        depthValue = depth(nodes[i])
        if depthValue > highestDepthValue:
            highestDepthValue = depthValue
            highestDepthValueNodeNumber = i
    print(nodes[highestDepthValueNodeNumber])


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



df = emp.groupby(['tag', 'user']).size().reset_index(name='counts')

df2 = df.groupby(['tag']).size().reset_index(name='usersPerTagCount')

dfTagsCount = df2.loc[df2['usersPerTagCount'] >= 500]

tagsWithCountedUsers = pd.merge(emp, dfTagsCount, on='tag', how='inner')
sortedByTS = tagsWithCountedUsers.sort_values(by=['ts'], ascending=True)
dupa = sortedByTS.groupby(['tag']).size().reset_index(name='usersPerTagCount')
print(dupa)


selectedTag = dupa.iloc[16]['tag']
sortedByTag = emp.loc[emp['tag'].str.strip() == selectedTag]
# print(sortedByTag)
nodesList = transformDFObjects2Node(sortedByTag)

nodesList.sort(key=lambda x: x.ts, reverse=False)
# for p in nodesList:
#     users = getFollowersListByUser(p.user, pfo)
#     print(users)
# print(nodes)

buildTree(nodesList)
