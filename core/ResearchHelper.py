import pickle as cPickle
import core.TagNode as TagNode
import core.EditDistance as EditDistance
import operator
import matplotlib.pyplot as plt
import networkx as nx
import zss
import copy
from itertools import islice

class NodeDistance(object):
    def __init__(self, TagNode, dist):
        self.TagNode = TagNode
        self.dist = dist

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def cutTreeByLevel(node, level):
    if not node.children:
        print("There are no children for this node.")

    nodesToCheck = []
    nodesToCheck.append(node)

    while nodesToCheck:
        currentNode = nodesToCheck.pop(0)
        for child in currentNode.children:
            if child.level > level:
                child.parent.children = []
                # print("Cutted in node: " + child.user)
                break
            else:
                nodesToCheck.append(child)

    return node

def cutTreeByTimestamp(node, timestamp):
    if not node.children:
        print("There are no children for this node.")

    nodesToCheck = []
    timestampStartValue = int(node.ts)
    nodesToCheck.append(node)

    while nodesToCheck:
        toRemove = list()
        currentNode = nodesToCheck.pop(0)
        for child in currentNode.children:
            if int(child.ts) - timestampStartValue > timestamp:
                child.children = []
                toRemove.append(child)
                # print("Cutted in node: " + child.user)
            else:
                nodesToCheck.append(child)

        for removable in toRemove:
            currentNode.children.remove(removable)

    return node

def checkSpreading(exampleTreeAfterCut, prototypes):

    nodeDistances = list()
    for index, prototypePackage in enumerate(prototypes):
        print("prototypes to compute: {0} ".format((len(prototypes) - index)))
        for prototype in prototypePackage:
            cuttedPrototype = cutTreeByLevel(copy.deepcopy(prototype), 3)
            # cuttedPrototype = cutTreeByTimestamp(copy.deepcopy(prototype), 1700000)
            dist = zss.simple_distance(
                exampleTreeAfterCut, cuttedPrototype, TagNode.Node.get_children, TagNode.Node.get_label2,
                EditDistance.weird_dist2)

            nodeDistances.append(NodeDistance(prototype, dist))

    nodeDistances.sort(key=lambda x: x.dist, reverse=False)
    filteredPrototypes = take(10, nodeDistances)

    for i, printable in enumerate(filteredPrototypes):
        print(filteredPrototypes[i].dist)

    return filteredPrototypes


def printTree(nodes, index):

    G = nx.DiGraph()

    #initialize root
    G.add_node(nodes.ts, tag=nodes.ts)


    nodesToCheck = []
    nodesToCheck.append(nodes)

    while nodesToCheck:
        currentNode = nodesToCheck.pop(0)
        for child in currentNode.children:
            G.add_node(child.ts, tag=child.ts)
            G.add_edge(currentNode.ts, child.ts, r=child.distance)
            nodesToCheck.append(child)

    G.nodes(data=True)

    # write dot file to use with graphviz
    # run "dot -Tpng test.dot >test.png"
    #nx.nx_pydot.write_dot(G, 'test.dot')

    nx.nx_pydot.write_dot(G, 'test.dot')

    # same layout using matplotlib with no labels
    plt.figure(figsize=(23, 12))
    plt.title(nodes.tag)
    pos = nx.nx_pydot.graphviz_layout(G, prog='dot', k=0.5)
    nx.draw(G, pos, node_size=30, node_color='b', font_size=8, with_labels=False, arrows=False)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.savefig('pictures/nx_test' + str(index) + '.png')

def printTreeForDifferences(exampleTree, exampleTreeAfterCut):
    G = nx.DiGraph()

    # initialize root
    G.add_node(exampleTree.ts, tag=exampleTree.ts)

    nodesToCheck = []
    exampleTreeAfterCutNodes = []
    nodesList = list()

    nodesToCheck.append(exampleTree)
    exampleTreeAfterCutNodes.append(exampleTreeAfterCut)

    # G.add_node(str(root.ts), tag=root.tag)

    while exampleTreeAfterCutNodes:
        currentNode = exampleTreeAfterCutNodes.pop(0)
        for child in currentNode.children:
            exampleTreeAfterCutNodes.append(child)
            nodesList.append(child)

    while nodesToCheck:
        currentNode = nodesToCheck.pop(0)
        for child in currentNode.children:
            G.add_node(child.ts, tag=child.ts)
            G.add_edge(currentNode.ts, child.ts, r=child.distance)
            nodesToCheck.append(child)

    nx.nx_pydot.write_dot(G, 'test.dot')

    # same layout using matplotlib with no labels
    plt.figure(figsize=(23, 12))
    plt.title(exampleTree.tag)
    pos = nx.nx_pydot.graphviz_layout(G, prog='dot', k=0.5)
    G.nodes(data=True)

    nx.draw(G, pos, node_size=30, font_size=8, with_labels=False, arrows=False)
    nx.draw(G, pos, node_size=50, nodelist=[exampleTree.ts], node_color='b', font_size=8, with_labels=False, arrows=False)
    nx.draw(G, pos, node_size=50, nodelist=[s.ts for s in nodesList], node_color='b', font_size=8, with_labels=False, arrows=False)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.savefig('pictures/prettyDiagramTest.png')



with open("C://Users//BKUCINSK//Documents//Docker//Magister//prototypes.pickle", 'rb') as prt:
    prototypes = cPickle.load(prt)

with open("C://Users//BKUCINSK//Documents//Docker//Magister//exampleTree.pickle", 'rb') as ext:
    exampleTree = cPickle.load(ext)

printTree(exampleTree, 1)
#
exampleTreeAfterDepthCut = cutTreeByLevel(copy.deepcopy(exampleTree), 3)
exampleTreeAfterTimeCut = cutTreeByTimestamp(copy.deepcopy(exampleTree), 1500000)
# #
printTree(exampleTreeAfterTimeCut, 2)
# printTree(exampleTreeAfterDepthCut, 2)
#
# printTreeForDifferences(exampleTree, exampleTreeAfterDepthCut)
#
#
# print(exampleTreeAfterTimeCut)

proposisions = checkSpreading(exampleTreeAfterDepthCut, prototypes)

for index, item in enumerate(proposisions):
    printTree(item.TagNode, index+5)

