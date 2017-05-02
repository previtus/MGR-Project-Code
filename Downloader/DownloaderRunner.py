# has function run with argument path, which will decide where its stored, also some basic settings, but nothing
# complicated - just an easy runner function
import Downloader.Defaults
from Downloader.PreprocessDataF import *
from Downloader.DataOperations import *
from Downloader.PreprocessData.SegmentsManipulators import *
from DatasetHandler.FileHelperFunc import *

def RunDownload(name, from_edge, to_edge, px_py):
    '''
    Run downloader while setting the most important variables here
    :param name: name of the folder it will safe in Data/StreetViewData/<name>
    :param from_edge: start with edge id
    :param to_edge: end with edge id
    :param px_py: pixels x and y - both same
    :return:
    '''
    print "Downloading data ", from_edge, to_edge, " into ", name

    path_to_edges = get_geojson_path()
    path_to_datafolder = get_project_folder()+'Data/StreetViewData/'+name+'/'
    make_folder_ifItDoesntExist(path_to_datafolder)

    print "edges at", path_to_edges
    print "into folder", path_to_datafolder

    FromEdgeID = from_edge
    ToEdgeID = to_edge
    PIXELS_X = px_py
    PIXELS_Y = px_py

    PreprocessDataF(path_to_edges, path_to_datafolder, FromEdgeID, ToEdgeID, PIXELS_X, PIXELS_Y)

    segments_file = path_to_datafolder+'/SegmentsData.dump'
    print "Downloaded, now checking"
    Segments = LoadDataFile(segments_file)
    StatisticsSegments(Segments)

    if (HasSomeErrorneousData(Segments, ERROR_MESSAGE_QUOTA)):
        print "Surpassed quota last lime! Redownloading."
        Segments = FixDataFile_FailedDownloads(segments_file, ERROR_MESSAGE_QUOTA, PIXELS_X, PIXELS_Y, path_to_datafolder)

    if (HasSomeErrorneousData(Segments, ERROR_MESSAGE_FAILED_MANY_TIMES)):
        print "Data had some errors, filling in the blanks!"
        Segments = FixDataFile_FailedDownloads(segments_file, ERROR_MESSAGE_FAILED_MANY_TIMES, PIXELS_X, PIXELS_Y, path_to_datafolder)
