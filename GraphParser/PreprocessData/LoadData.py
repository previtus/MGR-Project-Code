# LoadData.py
import time
from Loaders import *
from Functions import *

def LoadData(EdgesFile, NodesFile):
    '''
    Load all egdes and nodes of graph.
    Edges from csv with structure:
        From Id,To Id,Road type,Surface,Relative popularity
    Nodes from csv with structure:
        Latitude,Latitude projected,Longitude,Longitude projected,Elevation
    '''

    start_time = time.time()

    # function from Loaders.py
    Edges = open_with_python_csv_list(EdgesFile)
    Nodes = open_with_python_csv_list(NodesFile)

    print "loaded edges: ", len(Edges)
    print "loaded nodes: ", len(Nodes)

    print("--- %s seconds ---" % round(time.time() - start_time, 2))
    print '\n'
    return [Edges, Nodes]
