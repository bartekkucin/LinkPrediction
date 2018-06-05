
# coding: utf-8

# In[1]:


class Node(object):
    def __init__(self, tag, user, ts):
        self.tag = tag
        self.user = user
        self.ts = ts
        self.distance = 0
        self.parent = None
        self.children = []
        self.level = 1

    def add_child(self, child):
        #child = Node(obj.tag, obj.user, obj.ts)
        child.parent = self
        child.set_distance(int(child.ts) - int(self.ts))
        #child.children = obj.children
        self.children.append(child)

    def add_child_with_values(self, tag, user, ts):
        child = Node(tag, user, ts)
        child.parent = self
        child.set_distance(int(child.ts) - int(self.ts))
        #child.children = obj.children
        self.children.append(child)

    def set_distance(self, distance):
        self.distance = distance

    def set_level(self, level):
        self.level = level

    @staticmethod
    def get_label(node):
        return node.ts

    @staticmethod
    def get_children(node):
        return node.children

    def get_rev_children(self):
        children = self.children[:]
        children.reverse()
        return children

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

