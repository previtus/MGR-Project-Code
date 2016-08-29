import csv
import time
from Loaders import *
from Functions import *
from GraphEdgeSegment import *
import urllib


api = open('../apicode.txt', 'r').read()

start_time = time.time()

Edges = open_with_python_csv_list(r'../../graph/edges_.csv')
Nodes = open_with_python_csv_list(r'../../graph/nodes_.csv')

print "loaded edges: ", len(Edges)
print Edges[:1]
print "loaded nodes: ", len(Nodes)
print Nodes[:1]

print("--- %s seconds ---" % round(time.time() - start_time, 2))
print '\n'


i = 0
filenames = []
verbose = False

for edge in Edges[:NumEdgesToProcess]:
    FromId = int(edge[0])
    ToId = int(edge[1])
    Popularity = edge[4]

    segment = GraphEdgeSegment(FromId, ToId, Nodes)
    if verbose: segment.displaySegment()

    if verbose: print url, '\n', filename, '\n'
    print filename
    
    filenames.append(filename)
    
    urllib.urlretrieve(url, filename)

    
    i += 1

print filenames


frames = 0
import imageio
with imageio.get_writer('animation.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
        frames += 1

print "Saved to animation.gif with <", frames, "> frames."
