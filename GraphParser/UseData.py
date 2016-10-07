# UseData.py
from GenerateGIFAnimation import *
from Defaults import *
from PreprocessDataF import *
from DataOperations import *

import os

if not(os.path.isfile(DATASTRUCTUREFILE)):
    print "Data file was not found, downloading it!"
    PreprocessDataF(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)

Segments = LoadDataFile(DATASTRUCTUREFILE)
#gifname = "".join(['animation_from_main_',str(FromEdgeID),'-',str(ToEdgeID),'.gif'])
#GenerateGIFAnimation(Segments, gifname)


FixDataFile_FailedDownloads('SegmentsData_withSomeFails1.dump', ERROR_MESSAGE_FAILED_MANY_TIMES)
