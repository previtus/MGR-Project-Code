# PreprocessDataF.py

from PreprocessData.GenListOfUrls import *
from PreprocessData.PrepSegments import *
from PreprocessData.DownloadUrlFilenameMap import *
import json

from Defaults import *
from DataOperations import *

import pickle

def PreprocessDataF(EdgesFile, Path, FromEdgeID = FromEdgeID, ToEdgeID=ToEdgeID,
                    PIXELS_X = PIXELS_X, PIXELS_Y = PIXELS_Y, minimal_length=20):
    OutputFile = Path+DATASTRUCTUREFILE

    # 1 data prep
    with open(EdgesFile) as f:
        EdgesGEOJSON = json.load(f)
    Segments = PrepSegments(EdgesGEOJSON, FromEdgeID, ToEdgeID)

    # 2 list of urls
    FilenameMap = GenListOfUrls(Segments,PIXELS_X,PIXELS_Y, PrependPath=Path, minimal_length=minimal_length)

    # 3 download from urls
    FailedDownloads = DownloadUrlFilenameMap(FilenameMap, Segments)

    # 4 save datastructure
    SaveDataFile(OutputFile, Segments)

    return FailedDownloads

#PreprocessDataF(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)
