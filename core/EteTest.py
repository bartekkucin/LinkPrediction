from ete3 import Tree


t1 = Tree('(((a,b),c), ((e, f), g));')
t2 = Tree('(((a,c),b), ((e, f), g));')

#rf, max_rf, common_leaves, parts_t1, parts_t2 = t1.robinson_foulds(t2)
rf, max_rf, common_leaves, parts_t1, parts_t2,  discarded_edges_t1, discarded_edges_t2 = t1.robinson_foulds(t2)

print(t1, t2)
print("RF distance is %s over a total of %s" %(rf, max_rf))
print("Partitions in tree2 that were not found in tree1:", parts_t1 - parts_t2)
print("Partitions in tree1 that were not found in tree2:", parts_t2 - parts_t1)