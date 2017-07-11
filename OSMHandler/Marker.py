# Marks loaded Segments with vector indicating what is around the location - it's nearby neighbourhood.
# Needs access to the DB.
# Will use ConnectionHandler to mark segments.

from OSMHandler.Checker import Check
from Downloader.Defaults import OSM_MARKING_VERSION
import numpy
import os.path

print "imported Marker.py, inside DB requiring section."
stopfile = '/home/ekmek/Desktop/Project II/stop_dir/stop.txt'

# global variable - we can reuse Marker
ConnHandler = None

def Mark(Segments, radius = 50, interval = None):
    '''
    Mark Segments with radius. Call MarkSegment on each Segment.
    :param Segments:
    :param radius: radius in meters
    :return:
    '''
    from OSMHandler.ConnectionHandlerObj import ConnectionHandler

    global ConnHandler
    if ConnHandler is None:
        ConnHandler = ConnectionHandler()

    ConnHandler.report()
    #if Check(Segments):
    #    print "Segments seem to be up to date, breaking."
    #    return True

    # Mark segments
    i = 0

    if interval is None:
        interval = [0, len(Segments)]

    print interval
    for Segment in Segments[interval[0] : interval[1]]:
        i += 1
        stop = checkForStopFile()
        is_marked = Segment.checkOSMVersion()


        print i, "th from", interval[1] - interval[0], "[stop ",stop,", is marked ",is_marked,"]", interval
        if not stop and not is_marked:
            MarkSegment(Segment, radius = radius)

def checkForStopFile():
    stopfile_present = os.path.isfile(stopfile)
    stop = stopfile_present
    return stop


def MarkSegment(Segment, radius = 50):
    '''
    Mark Segment with new OSM vector depending on what the PosgreSQL db will tell us about the neighborhood.
    :param Segment: One Segment object initially without OSM data.
    :param radius: radius in meters
    :return:
    '''
    index = 0
    for distinctLocation in Segment.DistinctLocations:
        print "We are in ", distinctLocation

        # we combine them here!
        table_names = ["planet_osm_line", "planet_osm_point", "planet_osm_polygon", "planet_osm_roads"]

        global ConnHandler

        cumulative_vector = []
        for table in table_names:
            [nearby_vector, _] = ConnHandler.query_location(location=[distinctLocation[1], distinctLocation[0]], radius=radius, table_name=table)
            if len(cumulative_vector) == 0:
                cumulative_vector = nearby_vector
            else:
                from operator import add
                cumulative_vector = map(add, cumulative_vector, nearby_vector)

        print len(nearby_vector), numpy.sum(nearby_vector), nearby_vector

        Segment.markWithVector(cumulative_vector, index, OSM_MARKING_VERSION)
        index += 1
    print Segment

def closeConnection():
    # Close connection please.
    global ConnHandler
    ConnHandler.close_connection()
    ConnHandler.report()
