import csv
import time
from Loaders import *
start_time = time.time()

Edges = open_with_python_csv_list(r'../../graph/edges_.csv')
Nodes = open_with_python_csv_list(r'../../graph/nodes_.csv')

print "loaded edges: ", len(Edges)
print Edges[:1]
print "loaded nodes: ", len(Nodes)
print Nodes[:1]

print("--- %s seconds ---" % round(time.time() - start_time, 2))

