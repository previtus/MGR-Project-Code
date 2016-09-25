# PrepSegments.py
from GraphEdgeSegment import *
from Defaults import *

def PrepSegments(Edges, Nodes):
    '''
    Creates datastructure of Segments from list of edges and list of nodes.
    Segment is object made from edge with connected nodes and necessary functions.
    Returns list of segments Segments[SegmentId] -> Segment
    '''

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
