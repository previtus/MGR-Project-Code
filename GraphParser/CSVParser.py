import csv
import time
start_time = time.time()

edges_file = open(r'../../graph/edges.csv')
nodes_file = open(r'../../graph/nodes.csv')
#edges_file = open(r'edges_small.csv')
#nodes_file = open(r'nodes_small.csv')

edges_reader = csv.reader(edges_file, skipinitialspace=True)
print edges_reader.next()

nodes_reader = csv.reader(nodes_file, skipinitialspace=True)
print nodes_reader.next()

# parse to have list Edges
# with indexes to node in Nodes

Edges = []
Nodes = []

for edge in edges_reader:
    #print edge
    Edges.append(edge)

for node in nodes_reader:
    #print node
    Nodes.append(node)

print "loaded edges: ", len(Edges)
print "loaded nodes: ", len(Nodes)


print("--- %s seconds ---" % round(time.time() - start_time, 2))
