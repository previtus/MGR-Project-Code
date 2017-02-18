import json
from ImageHelpers import *
from Defaults import *
from PreprocessData.PrepSegments import *
from PreprocessData.GraphEdgeSegment import *

edges = 0
nodes = 0
with open(EDGESFILES_GEOJSON) as f:
    edges = json.load(f)
with open(NODESFILES_GEOJSON) as f:
    nodes = json.load(f)

print "Total edges:", len(edges['features'])


Segments = PrepSegments(edges)

print "Loaded:", len(Segments)