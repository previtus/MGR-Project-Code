# PrepSegments.py
from GraphEdgeSegment import *
import sys
sys.path.append('..')
from Defaults import *

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