# PreprocessData.py

from PreprocessData.LoadData import *
from PreprocessData.GenListOfUrls import *
from PreprocessData.PrepSegments import *
from PreprocessData.DownloadUrlFilenameMap import *
from Defaults import *

import pickle

def PreprocessData(EdgesFile, NodesFile, OutputFile):
    # 1 data prep
    [Edges, Nodes] = LoadData(EdgesFile, NodesFile)
    Segments = PrepSegments(Edges, Nodes)

    # 2 list of urls
    FilenameMap = GenListOfUrls(Segments)

    # 3 download from urls
    FailedDownloads = DownloadUrlFilenameMap(FilenameMap, Segments)

    # 4 save datastructure
    with open(OutputFile, 'wb') as f:
        pickle.dump(Segments, f)
    
    return FailedDownloads

#PreprocessData(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)
