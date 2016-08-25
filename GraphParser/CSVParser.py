import csv
import time
from Loaders import *
import pandas
start_time = time.time()


edges_reader = open_with_python_csv_list(r'../../graph/edges_.csv')
nodes_reader = open_with_python_csv_list(r'../../graph/nodes_.csv')

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
