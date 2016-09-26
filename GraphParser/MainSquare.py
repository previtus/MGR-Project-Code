from PreprocessData.LoadData import *
from PreprocessData.GenListOfUrls import *
from PreprocessData.PrepSegments import *
from PreprocessData.DownloadUrlFilenameMap import *
from PreprocessData.GenerateGIFAnimation import *
from PreprocessData.Defaults import *

import pickle

# 1 data prep
[Edges, Nodes] = LoadData()
Segments = PrepSegments(Edges, Nodes)

# 2 list of urls
FilenameMap = GenListOfUrls(Segments)

print "segments before downloading: "
for Segment in Segments[0:5]:
    Segment.displaySegmentShort()

# 3 download from urls
FailedDownloads = DownloadUrlFilenameMap(FilenameMap, Segments)

print "segments after downloading: "
for Segment in Segments[0:5]:
    Segment.displaySegmentShort()

# 4 process images (gif animation / whatever)
gifname = "".join(['animation_from_main_',str(FromEdgeID),'-',str(ToEdgeID),'.gif'])
GenerateGIFAnimation(Segments, gifname)

# Saving with PICKLE works:
#with open('test_out.dump', 'wb') as f:
#    pickle.dump(Segments, f)
