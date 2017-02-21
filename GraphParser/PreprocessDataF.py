# PreprocessDataF.py

from PreprocessData.GenListOfUrls import *
from PreprocessData.PrepSegments import *
from PreprocessData.DownloadUrlFilenameMap import *
import json

from Defaults import *
from DataOperations import *

import pickle

def PreprocessDataF(EdgesFile, OutputFile):
    # 1 data prep
    with open(EdgesFile) as f:
        EdgesGEOJSON = json.load(f)
    Segments = PrepSegments(EdgesGEOJSON)

    # 2 list of urls
    FilenameMap = GenListOfUrls(Segments)

    # 3 download from urls
    FailedDownloads = DownloadUrlFilenameMap(FilenameMap, Segments)

    # 4 save datastructure
    SaveDataFile(OutputFile, Segments)

    return FailedDownloads

#PreprocessDataF(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)
