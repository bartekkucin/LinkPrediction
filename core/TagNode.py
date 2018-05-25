
# coding: utf-8

# In[1]:


class Node(object):
    def __init__(self, tag, user, ts):
        self.tag = tag
        self.user = user
        self.ts = ts
        self.distance = 0
        self.children = []

    def add_child(self, obj):
        child = Node(obj.tag, obj.user, obj.ts)
        child.set_distance(int(child.ts) - int(self.ts))
        child.children = obj.children
        self.children.append(child)

    def set_distance(self, distance):
        self.distance = distance

    @staticmethod
    def get_label(node):
        return node.ts

    @staticmethod
    def get_children(node):
        return node.children

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.user) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'
        
def make_node(tag, user, ts):
    node = Node(tag, user, ts)
    return node

