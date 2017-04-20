# Marks loaded Segments with vector indicating what is around the location - it's nearby neighbourhood.
# Needs access to the DB.
# Will use ConnectionHandler to mark segments.

from OSMHandler.Checker import Check
from Downloader.Defaults import OSM_MARKING_VERSION

print "imported Marker.py, inside DB requiring section."

# global variable - we can reuse Marker
ConnHandler = None

def Mark(Segments):
    from OSMHandler.ConnectionHandlerObj import ConnectionHandler

    global ConnHandler
    if ConnHandler is None:
        ConnHandler = ConnectionHandler()

    ConnHandler.report()
    if Check(Segments):
        print "Segments seem to be up to date, breaking."
        return True

    # Mark segments
    for Segment in Segments:
        MarkSegment(Segment)

def MarkSegment(Segment):
    index = 0
    for distinctLocation in Segment.DistinctLocations:
        print "We are in ", distinctLocation

        # we mark it here!
        # >>build_sql_command_REWRITE
        nearby_vector = []

        Segment.DistinctNearbyVector[index] = nearby_vector

        Segment.Segment_OSM_MARKING_VERSION = OSM_MARKING_VERSION
        index += 1
    print Segment

def closeConnection():
    global ConnHandler
    ConnHandler.close_connection()
    ConnHandler.report()
