# PreprocessDataF.py
from PreprocessData.PrepSegments import *
import json

from DataOperations import *

def PreprocessDataFiles(EdgesFile, Path, FromEdgeID = FromEdgeID, ToEdgeID=ToEdgeID,
                        PIXELS_X = PIXELS_X, PIXELS_Y = PIXELS_Y, minimal_length=20, custom=False):
    # Preprocess data from files - used when downloading data.
    OutputFile = Path+DATASTRUCTUREFILE

    # 1 data prep
    with open(EdgesFile) as f:
        EdgesGEOJSON = json.load(f)
    Segments = PrepSegments(EdgesGEOJSON, FromEdgeID, ToEdgeID)

    print len(Segments)

    # 2 list of urls
    FilenameMap = GenListOfUrls(Segments,PIXELS_X,PIXELS_Y, PrependPath=Path, minimal_length=minimal_length, custom=custom)
    print len(FilenameMap)

    if not custom:
        # 3 download from urls
        FailedDownloads = DownloadUrlFilenameMap(FilenameMap, Segments)
    else:
        FailedDownloads = None

        # 4 save datastructure
    SaveDataFile(OutputFile, Segments)

    return FailedDownloads

#PreprocessDataFiles(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)
