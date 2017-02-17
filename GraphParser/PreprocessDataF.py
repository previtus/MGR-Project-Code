# PreprocessDataF.py

from PreprocessData.LoadData import *
from PreprocessData.GenListOfUrls import *
from PreprocessData.PrepSegments import *
from PreprocessData.DownloadUrlFilenameMap import *
from PreprocessData.ScoreData import *
import json

from Defaults import *
from DataOperations import *

import pickle

def PreprocessDataF(EdgesFile, NodesFile, OutputFile):
    # 1 data prep
    DataMethod = 'NEW' # 'NEW' or 'OLD'
    if DataMethod == 'OLD':
        [Edges, Nodes] = LoadData(EdgesFile, NodesFile)
        Segments = PrepSegments(Edges, Nodes)
    elif DataMethod == 'NEW':
        with open(EDGESFILES_GEOJSON) as f:
            EdgesGEOJSON = json.load(f)
        Segments = PrepSegments(EdgesGEOJSON)

    # 2 list of urls
    FilenameMap = GenListOfUrls(Segments)

    # 3 download from urls
    FailedDownloads = DownloadUrlFilenameMap(FilenameMap, Segments)

    # (temporary) enrich data with score
    if DataMethod == 'OLD':
        ScoreData(Segments)

    # 4 save datastructure
    SaveDataFile(OutputFile, Segments)
    
    return FailedDownloads

#PreprocessDataF(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)
