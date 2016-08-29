import time
from Loaders import *
from Functions import *

def LoadData():
    api = getApi();

    start_time = time.time()

    Edges = open_with_python_csv_list(r'../../graph/edges_.csv')
    Nodes = open_with_python_csv_list(r'../../graph/nodes_.csv')

    print "loaded edges: ", len(Edges)
    print "loaded nodes: ", len(Nodes)

    print("--- %s seconds ---" % round(time.time() - start_time, 2))
    print '\n'
    return [Edges, Nodes]
