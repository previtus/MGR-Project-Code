import json
from Omnipresent import len_
import Downloader.DataOperations as DataOperations
from Downloader import KerasPreparation
import os
import numpy as np

from DatasetHandler.FileHelperFunc import get_project_folder
ABS_PATH_TO_PRJ = get_project_folder()

# path_to_streetview_folder = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/'
#path_to_streetview_folder = "/home/ekmek/Vitek/Mgr project/MGR-Project-Code/Data/StreetViewData/"
path_to_streetview_folder = ABS_PATH_TO_PRJ + 'Data/StreetViewData/'
name_of_segments_file = "5556x_markable_640x640/SegmentsData_marked_R100_4Tables.dump"


def loadGeoJson(path):
    ''' Load GeoJSON file '''
    with open(path) as f:
        GeoJSON = json.load(f)
    return GeoJSON

def saveGeoJson(GeoJSON, path):
    ''' Save GeoJSON file '''
    print "Saving GeoJSON object to:", path
    with open(path, 'a') as f:
        json.dump(GeoJSON, f)

def loadDefaultGEOJSON():
    ''' Load default GeoJSON file, which is the initial attractivity_previtus_data_1_edges.geojson file '''
    from DatasetHandler.FileHelperFunc import get_geojson_path
    path = get_geojson_path()
    return loadGeoJson(path)

def internalToExternal(score):
    ''' Convert score notations back to how geojson file used it. '''
    if score <> -1:
        return int(round(score * 100))
    return score

def markGeoJSON(GeoJSON, Segments):
    '''
    Mark geojson object with data from corresponding Segment object in Segments
    :param GeoJSON: geojson object
    :param Segments: list of objects
    :return: altered GeoJSON object
    '''
    SegmentId = 0
    for feature in GeoJSON['features']:
        if (feature['geometry']['type'] == 'LineString'):
            if 'attractivity' in feature['properties']:
                json_score = feature['properties']['attractivity']
            else:
                json_score = -1

            if SegmentId < len(Segments):
                internal_score = Segments[SegmentId].getScore()
                segments_score = internalToExternal(internal_score)

                feature['properties']['attractivity'] = segments_score

            SegmentId += 1

    return GeoJSON

def traverseGeoJSON(GeoJSON, Segments):
    '''
    For testing purposes we go through all entries in GeoJSON and check for scores in Segments,
    we report the altered values.
    :param GeoJSON:
    :param Segments:
    :return:
    '''
    SegmentId = 0
    for feature in GeoJSON['features']:
        if (feature['geometry']['type'] == 'LineString'):
            if 'attractivity' in feature['properties']:
                json_score = feature['properties']['attractivity']
            else:
                json_score = -1

            if SegmentId < len(Segments):
                internal_score = Segments[SegmentId].getScore()
                segments_score = internalToExternal(internal_score)

                if json_score <> segments_score:
                    print SegmentId, json_score, segments_score

            #Coordinates = feature['geometry']['coordinates']
            #Start = tuple([Coordinates[0][1], Coordinates[0][0]])
            #End = tuple([Coordinates[-1][1], Coordinates[-1][0]])

            #segment = SegmentObj(Start, End, Score, SegmentId)
            #if verbose: segment.displaySegment()
            SegmentId += 1

def prepEvaluatedData(y_pred, segment_ids):
    ''' prepare dictionary which will give us scores of certain segment id all clustered together into one list. '''
    EvaluatedData = {}
    for i in range(0,len(y_pred)):
        id = segment_ids[i]
        predicted_score = y_pred[i]
        if id in EvaluatedData:
            EvaluatedData[id].append(predicted_score)
        else:
            EvaluatedData[id] = [predicted_score]
    return EvaluatedData

def AlterSegments(EvaluatedData, Segments, only_unknown_scores=True):
    '''
    Edit internal values of Segments depending on what data we got.
    :param EvaluatedData: processed dictionary which can give us list of values for segment id
    :param Segments: list of Segment objects, which we iterate through and change their scores.
    :param only_unknown_scores: Flag whether we overwrite only those Segments which had unknown score in
    the initial dataset.
    :return: Altered Segments list
    '''
    SegmentId = 0
    for SegmentId in range(0, len(Segments)):
        Segment = Segments[SegmentId]
        has_no_score = Segment.hasUnknownScore()
        internal_score = Segments[SegmentId].getScore()

        mark = False

        if only_unknown_scores:
            if has_no_score:
                mark = True
        if not only_unknown_scores:
            mark = True

        if mark:
            if SegmentId in EvaluatedData:
                scores = EvaluatedData[SegmentId]
                avg_score = np.mean(scores)

                Segment.Score = avg_score

    return Segments

def loadDataFromSegments(path_to_segments_file, SCORE, verbose=False, we_dont_care_about_missing_images=False):
    '''
    Load lists from Segments
    :param path_to_segments_file: Segments file to be loaded.
    :param SCORE: flag for if we care for only scored Segments
    :param verbose:
    :param we_dont_care_about_missing_images: flag for if we care for only those Segments with images
    (OSM model doesnt need them.)
    :return: lists and Segments
    '''
    Segments = DataOperations.LoadDataFile(path_to_segments_file)
    segments_dir = os.path.dirname(path_to_segments_file) + '/'
    __list_of_images, __labels, __osm, __segment_ids, flag_is_extended = KerasPreparation.LoadDataFromSegments(Segments, has_score=SCORE, path_to_images=segments_dir, we_dont_care_about_missing_images=we_dont_care_about_missing_images)

    if verbose:
        print "__list_of_images", len_(__list_of_images), __list_of_images[0:5]
        print "__labels", len_(__labels), __labels[0:5]
        print "__osm", len_(__osm)
        print "__segment_ids", len_(__segment_ids), __segment_ids[0:5]
        print "flag_is_extended", flag_is_extended

    return [__list_of_images, __labels, __osm, __segment_ids], Segments

def small_lists(lists, n=50):
    '''
    Subset of first n values.
    :param lists:
    :param n:
    :return: subsets of lists
    '''
    small = []
    for item in lists:
        small.append(item[0:n])
    return small

def analyze_lists(lists):
    '''
    Analyze statistics inside lists. Count for unique segments and numbers of images.
    :param lists:
    :return:
    '''
    __list_of_images, __labels, __osm, __segment_ids = lists
    number_of_images = len(__list_of_images)
    number_of_images_without_score = 0
    number_of_segments = 0
    number_of_segments_without_score = 0

    unique_segment_ids = []
    scoreless_segment_ids = []


    n = min([len(__list_of_images), len(__labels), len(__segment_ids)])

    for i in range(0, n):
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
    print "Scored ", (number_of_segments-number_of_segments_without_score), " Segments with", (number_of_images-number_of_images_without_score), "images."

def osm_from_lists(lists):
    ''' Get osm data '''
    __list_of_images, __labels, __osm, __segment_ids = lists
    osm = np.asarray(__osm)
    return osm

#### GENERATORS
def getImgGenerator_from_lists(lists):
    '''
    Create generator on given list, yielding imagery data.
    :param lists:
    :return:
    '''
    __list_of_images, __labels, __osm, __segment_ids = lists

    size = len(__list_of_images)
    order = range(size)

    image_generator = generator_img(order, image_paths=__list_of_images)
    return [order, image_generator, size]

def getOsmGenerator_from_lists(lists):
    '''
    Create generator on given list, yielding vector data.
    :param lists:
    :return:
    '''
    __list_of_images, __labels, __osm, __segment_ids = lists

    size = len(__list_of_images)
    order = range(size)

    osm_generator = generator_osm(order, osms=__osm)
    return [order, osm_generator, size]

def generator_img(order, image_paths, resize=None):
    ''' generator yields loaded images one by one, needed to save memory '''
    while True:
        for index in order:
            image = KerasPreparation.LoadActualImages([image_paths[index]], resize=resize)
            yield (image)
def generator_osm(order, osms):
    ''' generator yields osm vectors one by one, not really needed '''
    while True:
        for index in order:
            osm = osms[index]
            yield (osm)

def default_segments_path():
    ''' assembles path to the segments files '''
    folder = path_to_streetview_folder
    path_to_segments_file = folder + name_of_segments_file

    return path_to_segments_file
