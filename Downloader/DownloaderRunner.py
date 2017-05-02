# has function run with argument path, which will decide where its stored, also some basic settings, but nothing
# complicated - just an easy runner function
from Downloader.Defaults import *
from Downloader.PreprocessDataF import *
from Downloader.DataOperations import *
from Downloader.PreprocessData.SegmentsManipulators import *
from DatasetHandler.FileHelperFunc import *

def RunDownload(name, from_edge, to_edge):
    print "Downloading data ", from_edge, to_edge, " into ", name
    
    path_to_edges = get_geojson_path()
    path_to_datafolder = get_project_folder()+'Data/StreetViewData/'+name
    make_folder_ifItDoesntExist(path_to_datafolder)

    segments_file = path_to_datafolder+'/SegmentsData.dump'

    print "edges at", path_to_edges
    print "segment at", segments_file

    '''
    PreprocessDataF(path_to_edges, DATASTRUCTUREFILE)

    print "Downloaded, now checking"
    Segments = LoadDataFile(DATASTRUCTUREFILE)
    StatisticsSegments(Segments)

    if (HasSomeErrorneousData(Segments, ERROR_MESSAGE_QUOTA)):
        print "Surpassed quota last lime! Redownloading."
        Segments = FixDataFile_FailedDownloads(DATASTRUCTUREFILE, ERROR_MESSAGE_QUOTA)

    if (HasSomeErrorneousData(Segments, ERROR_MESSAGE_FAILED_MANY_TIMES)):
        print "Data had some errors, filling in the blanks!"
        Segments = FixDataFile_FailedDownloads(DATASTRUCTUREFILE, ERROR_MESSAGE_FAILED_MANY_TIMES)
    '''

RunDownload("georgetown", 0, 1000)
