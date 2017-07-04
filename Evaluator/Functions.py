import json
from Omnipresent import len_
import Downloader.DataOperations as DataOperations
from Downloader import KerasPreparation
import os

def loadGeoJson(path):
    with open(path) as f:
        GeoJSON = json.load(f)
    return GeoJSON

def saveGeoJson(GeoJSON, path):
    print "Saving GeoJSON object to:", path
    with open(path, 'a') as f:
        json.dump(GeoJSON, f)

def loadDefaultGEOJSON():
    from DatasetHandler.FileHelperFunc import get_geojson_path
    path = get_geojson_path()
    return loadGeoJson(path)

def internalToExternal(score):
    if score <> -1:
        return int(round(score * 100))
    return score

def tmpMarkGeoJSON(GeoJSON, Segments):
    SegmentId = 0
    for feature in GeoJSON['features']:
        if (feature['geometry']['type'] == 'LineString'):
            json_score = feature['properties']['attractivity']
            internal_score = Segments[SegmentId].getScore()
            segments_score = internalToExternal(internal_score)

            if json_score == -1:
                feature['properties']['attractivity'] = 200

            SegmentId += 1

    return GeoJSON

def traverseGeoJSON(GeoJSON, Segments):
    SegmentId = 0
    for feature in GeoJSON['features']:
        if (feature['geometry']['type'] == 'LineString'):
            json_score = feature['properties']['attractivity']
            internal_score = Segments[SegmentId].getScore()
            segments_score = internalToExternal(internal_score)

            if json_score <> segments_score:
                print SegmentId, json_score, segments_score

            Coordinates = feature['geometry']['coordinates']
            Start = tuple([Coordinates[0][1], Coordinates[0][0]])
            End = tuple([Coordinates[-1][1], Coordinates[-1][0]])

            #segment = SegmentObj(Start, End, Score, SegmentId)
            #if verbose: segment.displaySegment()
            SegmentId += 1

'''
def UnknownSegmentsSubset(Segments):
    SegmentId = 0
    for SegmentId in range(0, len(Segments)):
        Segment = Segments[SegmentId]
        has_score = Segment.hasUnknownScore()

        internal_score = Segments[SegmentId].getScore()

        print internal_score
'''

def loadDataFromSegments(path_to_segments_file, SCORE, verbose=False):
    Segments = DataOperations.LoadDataFile(path_to_segments_file)
    segments_dir = os.path.dirname(path_to_segments_file) + '/'
    __list_of_images, __labels, __osm, __segment_ids, flag_is_extended = KerasPreparation.LoadDataFromSegments(Segments, has_score=SCORE, path_to_images=segments_dir)

    if verbose:
        print "__list_of_images", len_(__list_of_images), __list_of_images[0:5]
        print "__labels", len_(__labels), __labels[0:5]
        print "__osm", len_(__osm)
        print "__segment_ids", len_(__segment_ids), __segment_ids[0:5]
        print "flag_is_extended", flag_is_extended

    return [__list_of_images, __labels, __osm, __segment_ids]

def filter_lists_only_unknown_score(lists, verbose):
    __list_of_images, __labels, __osm, __segment_ids = lists

    f__list_of_images, f__labels, f__osm, f__segment_ids = [[],[],[],[]]
    for i in range(0, len(__list_of_images)):
        if __labels[i] == -1:
            f__list_of_images.append(__list_of_images[i])
            f__labels.append(__labels[i])
            f__osm.append(__osm[i])
            f__segment_ids.append(__segment_ids[i])

    if verbose:
        print "f__list_of_images", len_(f__list_of_images), f__list_of_images[0:5]
        print "f__labels", len_(f__labels), f__labels[0:5]
        print "f__osm", len_(f__osm)
        print "f__segment_ids", len_(f__segment_ids), f__segment_ids[0:5]

    return [f__list_of_images, f__labels, f__osm, f__segment_ids]

def analyze_lists(lists):
    __list_of_images, __labels, __osm, __segment_ids = lists
    number_of_images = len(__list_of_images)
    number_of_images_without_score = 0
    number_of_segments = 0
    number_of_segments_without_score = 0

    unique_segment_ids = []
    scoreless_segment_ids = []

    for i in range(0, len(__list_of_images)):
        id = __segment_ids[i]
        if id not in unique_segment_ids:
            unique_segment_ids.append(id)
        if __labels[i] == -1:
            number_of_images_without_score += 1
            if id not in scoreless_segment_ids:
                scoreless_segment_ids.append(id)

    number_of_segments = len(unique_segment_ids)
    number_of_segments_without_score = len(scoreless_segment_ids)

    print "Lists contain", number_of_segments, "of Segments with", number_of_images, "images."
    print "Unscored ", number_of_segments_without_score, " Segments with", number_of_images_without_score, "images."


def main():

    #GeoJSON = loadDefaultGEOJSON()
    #print GeoJSON.keys()

    folder = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/'
    path_to_segments_file = folder + '5556x_minlen30_640px/SegmentsData_marked_R100_4Tables.dump'
    path_to_segments_file = folder + '5556x_markable_640x640/SegmentsData_marked_R100.dump'

    '''
    Segments = DataOperations.LoadDataFile(path_to_segments_file)

    traverseGeoJSON(GeoJSON, Segments)


    evaluated_geojson = tmpMarkGeoJSON(GeoJSON, Segments)
    path_geojson_out = 'temp.geojson'
    saveGeoJson(evaluated_geojson, path_geojson_out)

    #traverseGeoJSON(a, Segments)
    '''

    lists = loadDataFromSegments(path_to_segments_file, None)

    analyze_lists(lists)


main()
