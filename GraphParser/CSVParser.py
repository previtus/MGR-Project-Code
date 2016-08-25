import csv
import time
from Loaders import *
start_time = time.time()

Edges = open_with_python_csv_list(r'../../graph/edges_first5.csv')
Nodes = open_with_python_csv_list(r'../../graph/nodes_.csv')

print "loaded edges: ", len(Edges)
print Edges[:1]
print "loaded nodes: ", len(Nodes)
print Nodes[:1]

print("--- %s seconds ---" % round(time.time() - start_time, 2))
print '\n'

NumEdgesToProcess = 4


class GraphEdgeSegment:
    'Common base class for all employees'
    tmp = 0
    
    def __init__(self, FromId, ToId, Nodes):
        self.FromId = FromId
        self.ToId = ToId
        self.Start = Nodes[FromId]
        self.End = Nodes[ToId]
        
        GraphEdgeSegment.tmp += 1
   
    def displaySegment(self):
        print "From: ", self.FromId,  ", To: ", self.ToId
        print "Start: ", self.Start
        print "End: ", self.End

    def getLocationStringStart(self):
        return "".join( [self.Start[0],",", self.Start[2]] )
    def getLocationStringEnd(self):
        return "".join( [self.End[0],",", self.End[2]] )



for edge in Edges[:NumEdgesToProcess]:
    FromId = int(edge[0])
    ToId = int(edge[1])
    Popularity = edge[4]

    segment = GraphEdgeSegment(FromId, ToId, Nodes)
    segment.displaySegment()
    print segment.getLocationStringStart()

    print ''#edge
