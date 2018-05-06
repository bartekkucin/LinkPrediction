class DepthSerializer(object):
    def __init__(self, depthValue, count):
        self.depthValue = depthValue
        self.count = count

def make_depthSerializer(depthValue, count):
    depthSerializer = DepthSerializer(depthValue, count)
    return depthSerializer
