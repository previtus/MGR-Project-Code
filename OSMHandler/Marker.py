# Marks loaded Segments with vector indicating what is around the location - it's nearby neighbourhood.
# Needs access to the DB.
# Will use ConnectionHandler to mark segments.

from OSMHandler.Checker import Check
from Downloader.Defaults import OSM_MARKING_VERSION

print "imported Marker.py, inside DB requiring section."

# global variable - we can reuse Marker
ConnHandler = None

def Mark(Segments, radius = 50):
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
        MarkSegment(Segment, radius = radius)

def MarkSegment(Segment, radius = 50):
    index = 0
    for distinctLocation in Segment.DistinctLocations:
        print "We are in ", distinctLocation

        # we mark it here!
        global ConnHandler
        [nearby_vector, _] = ConnHandler.query_location(location=[distinctLocation[1], distinctLocation[0]], radius=radius)
        print len(nearby_vector), nearby_vector

        Segment.markWithVector(nearby_vector, index, OSM_MARKING_VERSION)
        index += 1
    print Segment

def closeConnection():
    global ConnHandler
    ConnHandler.close_connection()
    ConnHandler.report()
