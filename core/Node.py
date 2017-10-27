
# coding: utf-8

# In[1]:


class Node(object):
    def __init__(self, tag, user, ts):
        self.tag = tag
        self.user = user
        self.ts = ts
        self.children = []

def add_child(self, obj):
        self.children.append(obj)
        
def make_node(tag, user, ts):
    node = Node(tag, user, ts)
    return node

