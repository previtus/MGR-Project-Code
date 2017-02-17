# PrepSegments.py
from GraphEdgeSegment import *
import sys
sys.path.append('..')
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

def PrepSegments(EdgesGEOJSON):
    '''
    Alternative loading method, which relies just upon edge data (we don't have nodes fully available this time).

    :param EdgesGEOJSON: Inputs the json object obtained via json.load(json_file)
    :return: Returns the whole set of Segments
    '''

    Segments = []

    SegmentId = FromEdgeID
    verbose = False

    for feature in EdgesGEOJSON['features'][FromEdgeID:ToEdgeID]:
        if (feature['geometry']['type'] == 'LineString'):
            Coordinates = feature['geometry']['coordinates']
            Score = feature['properties']['attractivity']

            Start = tuple([Coordinates[0][1], Coordinates[0][0]])
            End = tuple([Coordinates[-1][1], Coordinates[-1][0]])

            segment = GraphEdgeSegment(Start, End, Score, SegmentId)
            if verbose: segment.displaySegment()
            SegmentId += 1

            Segments.append(segment)
        else:
            print feature

    return Segments