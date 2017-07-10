# PrepSegments.py
from SegmentObj import *
import sys
sys.path.append('..')

from Downloader.Defaults import *

def PrepSegments(EdgesGEOJSON, FromEdgeID = FromEdgeID, ToEdgeID=ToEdgeID):
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
            if "attractivity" in feature['properties']:
                Score = feature['properties']['attractivity']
            else:
                Score = -1

            Start = tuple([Coordinates[0][1], Coordinates[0][0]])
            End = tuple([Coordinates[-1][1], Coordinates[-1][0]])

            segment = SegmentObj(Start, End, Score, SegmentId)
            if verbose: segment.displaySegment()
            SegmentId += 1

            Segments.append(segment)
        else:
            print feature

    return Segments
