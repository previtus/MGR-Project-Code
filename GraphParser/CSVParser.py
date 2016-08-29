import csv
import time
from Loaders import *
from Functions import *


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

        # Latitude,Latitude projected,Longitude,Longitude projected,Elevation
        #self.Start = map(float, Nodes[FromId])
        #self.End = map(float, Nodes[ToId])
        self.Start = ( float(Nodes[FromId][0]), float(Nodes[FromId][2]) )
        self.End = ( float(Nodes[ToId][0]), float(Nodes[ToId][2]) )

        self.ProjectedStart = ( float(Nodes[FromId][1]), float(Nodes[FromId][3]) )
        self.ProjectedEnd = ( float(Nodes[ToId][1]), float(Nodes[ToId][3]) )
        
        self.ElevationStart = float(Nodes[FromId][4])
        self.ElevationEnd = float(Nodes[ToId][4])
        
        GraphEdgeSegment.tmp += 1
   
    def displaySegment(self):
        print "From: ", self.FromId,  ", To: ", self.ToId
        print "Start: ", self.Start
        print "End: ", self.End

    def getBearingString(self):
        return bearing_between_two_points(self.Start, self.End)


for edge in Edges[:NumEdgesToProcess]:
    FromId = int(edge[0])
    ToId = int(edge[1])
    Popularity = edge[4]

    segment = GraphEdgeSegment(FromId, ToId, Nodes)
    segment.displaySegment()
    print segment.getBearingString()

    print ''#edge
