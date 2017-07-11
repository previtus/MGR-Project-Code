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

def Mark(Segments, radius = 50, interval = None, backwards=False):
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

    if interval is None:
        interval = [0, len(Segments)]

    if backwards:
        indices = range(interval[1]-1, interval[0]-1, -1)
    else:
        indices = range(interval[0], interval[1])

    i = 0
    print interval
    for index in indices:
        Segment = Segments[index]
        i += 1
        stop = checkForStopFile()
        is_marked = Segment.checkOSMVersion()


        print i, "th from", interval[1] - interval[0], "[stop ",stop,", is marked ",is_marked,"]", interval, "index=", index
        if not stop and not is_marked:
            MarkSegment(Segment, radius = radius)

        Segments[index] = Segment

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

def MergeMarking_LoadAndSave(pats_seg1, path_seg2, path_out):
    import Downloader.DataOperations

    Segments1 = Downloader.DataOperations.LoadDataFile(pats_seg1)
    Segments2 = Downloader.DataOperations.LoadDataFile(path_seg2)

    MergedSegments = MergeMarking(Segments1, Segments2)

    Downloader.DataOperations.SaveDataFile(path_out, MergedSegments)

def MergeMarking(Segments1, Segments2):
    print "Merging labeling from two segments files, lens:", len(Segments1), len(Segments2)
    if len(Segments1) <> len(Segments2):
        return None

    for i in range(0, len(Segments1)):
        S1 = Segments1[i]
        S2 = Segments2[i]

        s1_is_marked = S1.checkOSMVersion()
        s2_is_marked = S2.checkOSMVersion()

        if not s1_is_marked and s2_is_marked:
            # mark s1 by the osms which are in s2!
            osm_version = S2.Segment_OSM_MARKING_VERSION
            for j in range(0,len(S2.DistinctNearbyVector)):
                nearby_vector = S2.DistinctNearbyVector[j]
                S1.markWithVector(nearby_vector, j, osm_version)

        Segments1[i] = S1

    return Segments1

"""
s1path = '/home/ekmek/Vitek/Mgr project/MGR-Project-Code/Data/StreetViewData/Prague_DOP_Cyklotrasy_l/SegmentsData_mark100_progress (376 th from 4073).dump'
s2path = '/home/ekmek/Vitek/Mgr project/MGR-Project-Code/Data/StreetViewData/Prague_DOP_Cyklotrasy_l/SegmentsData_fromBack.dump'
s_merged = '/home/ekmek/Vitek/Mgr project/MGR-Project-Code/Data/StreetViewData/Prague_DOP_Cyklotrasy_l/SegmentsData_MERGED.dump'

MergeMarking_LoadAndSave(s1path, s2path, s_merged)
"""