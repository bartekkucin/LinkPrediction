import zss

try:
    from editdist import distance as strdist
except ImportError:
    def strdist(a, b):
        # calculateSimilarity

        if a != "" and b != "":
            if calculateSimilarity(int(a), int(b)):
                return 0
            else:
                return 1
        else:
            if a == b:
                return 0
            else:
                return 1

    def strdist2(a, b):

            if a == b:
                return 0
            else:
                if a != "" and b != "":
                    if calculateSimilarity(int(a), int(b)):
                        return 0

                return 1

def weird_dist(NodeA, NodeB):
    return 10*strdist(NodeA, NodeB)

def weird_dist2(NodeA, NodeB):
    return 10*strdist2(NodeA, NodeB)

def calculateSimilarity(a, b) :
    distance = a - b
    if(distance > 100):
        return False
    return True



