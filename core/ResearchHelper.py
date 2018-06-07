import pickle as cPickle
import core.TagNode as TagNode
import core.EditDistance as EditDistance
import operator
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

def calculateEditDistanceWithPrototypes(exampleTreeAfterCut, prototypes):

    nodeDistances = list()
    for index, prototypePackage in enumerate(prototypes):
        print("prototypes to compute: {0} ".format((len(prototypes) - index)))
        for prototype in prototypePackage:
            cuttedPrototype = cutTreeByLevel(copy.deepcopy(prototype), 3)
            dist = zss.simple_distance(
                exampleTreeAfterCut, cuttedPrototype, TagNode.Node.get_children, TagNode.Node.get_label2,
                EditDistance.weird_dist2)

            nodeDistances.append(NodeDistance(prototype, dist))

        # if(index == 50):
        #     break

    nodeDistances.sort(key=lambda x: x.dist, reverse=False)
    filteredPrototypes = take(10, nodeDistances)

    for i, printable in enumerate(filteredPrototypes):
        print(filteredPrototypes[i].TagNode)




with open("C://Users//BKUCINSK//Documents//Docker//Magister//Badania//prototypes.pickle", 'rb') as prt:
    prototypes = cPickle.load(prt)

with open("C://Users//BKUCINSK//Documents//Docker//Magister//Badania//exampleTree.pickle", 'rb') as ext:
    exampleTree = cPickle.load(ext)

exampleTreeAfterCut = cutTreeByLevel(copy.deepcopy(exampleTree), 3)
calculateEditDistanceWithPrototypes(exampleTreeAfterCut, prototypes)

print("prototyp")

print(exampleTreeAfterCut)