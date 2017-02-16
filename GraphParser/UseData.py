# UseData.py
from GenerateGIFAnimation import *
from Defaults import *
from PreprocessDataF import *
from DataOperations import *

import os

if not(os.path.isfile(DATASTRUCTUREFILE)):
    print "Data file was not found, downloading it!"
    PreprocessDataF(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)

# TODO: Allow for random downloading - specifying that I want N=1000 valid segments, but they should be taken randomly (uniformly from the 0-1165640

Segments = LoadDataFile(DATASTRUCTUREFILE)

if (HasSomeErrorneousData(Segments, ERROR_MESSAGE_FAILED_MANY_TIMES)):
    print "Data had some errors, filling in the blanks!"
    Segments = FixDataFile_FailedDownloads(DATASTRUCTUREFILE, ERROR_MESSAGE_FAILED_MANY_TIMES)

#gifname = "".join(['animation_from_main_',str(FromEdgeID),'-',str(ToEdgeID),'.gif'])
#GenerateGIFAnimation(Segments, gifname)


