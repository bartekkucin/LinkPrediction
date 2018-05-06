
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
        self.children.append(obj)

    def set_distance(self, distance):
        self.distance = distance

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

