from LoadData import *
from GenListOfUrls import *
from PrepSegments import *


# 1 data prep
[Edges, Nodes] = LoadData()
Segments = PrepSegments(Edges, Nodes)

# 2 list of urls
FilenameMap = GenListOfUrls(Segments)

# 3 download from urls
print FilenameMap

# 4 process images (gif animation / whatever)
