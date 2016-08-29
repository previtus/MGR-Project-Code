from GraphEdgeSegment import *
from Defaults import *

def PrepSegments(Edges, Nodes):

    Segments = []
    
    SegmentId = FromEdgeID
    verbose = False

    for edge in Edges[FromEdgeID:ToEdgeID]:
        FromId = int(edge[0])
        ToId = int(edge[1])
        Popularity = edge[4]

        segment = GraphEdgeSegment(FromId, ToId, Nodes, SegmentId)
        if verbose: segment.displaySegment()
        SegmentId += 1

        Segments.append(segment)

    return Segments
