from LoadData import *
from GenListOfUrls import *
from PrepSegments import *
from DownloadUrlFilenameMap import *
from GenerateGIFAnimation import *

# 1 data prep
[Edges, Nodes] = LoadData()
Segments = PrepSegments(Edges, Nodes)

# 2 list of urls
FilenameMap = GenListOfUrls(Segments)

# 3 download from urls
DownloadUrlFilenameMap(FilenameMap)

# 4 process images (gif animation / whatever)
GenerateGIFAnimation(FilenameMap, 'animation_from_main.gif')
