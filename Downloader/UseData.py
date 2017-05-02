# UseData.py
from Downloader.GenerateGIFAnimation import *
from Downloader.Defaults import *
from Downloader.PreprocessDataF import *
from Downloader.DataOperations import *
from Downloader.PreprocessData.SegmentsManipulators import *
import os

if not(os.path.isfile(DATASTRUCTUREFILE)):
    print "Data file was not found, downloading it!"
    PreprocessDataF(EDGESFILES_GEOJSON, '', FromEdgeID, ToEdgeID, PIXELS_X, PIXELS_Y)

Segments = LoadDataFile(DATASTRUCTUREFILE)
StatisticsSegments(Segments)

if (HasSomeErrorneousData(Segments, ERROR_MESSAGE_QUOTA)):
    print "Surpassed quota last lime! Redownloading."
    Segments = FixDataFile_FailedDownloads(DATASTRUCTUREFILE, ERROR_MESSAGE_QUOTA)

if (HasSomeErrorneousData(Segments, ERROR_MESSAGE_FAILED_MANY_TIMES)):
    print "Data had some errors, filling in the blanks!"
    Segments = FixDataFile_FailedDownloads(DATASTRUCTUREFILE, ERROR_MESSAGE_FAILED_MANY_TIMES)

#gifname = "".join(['animation_from_main_',str(FromEdgeID),'-',str(ToEdgeID),'.gif'])
#GenerateGIFAnimation(Segments, gifname)
