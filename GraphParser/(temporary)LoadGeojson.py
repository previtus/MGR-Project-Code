import json
from ImageHelpers import *
from Defaults import *
from PreprocessData.GraphEdgeSegment import *

edges = 0
nodes = 0
with open(EDGESFILES_GEOJSON) as f:
    edges = json.load(f)
with open(NODESFILES_GEOJSON) as f:
    nodes = json.load(f)

print len(edges['features'])

for feature in edges['features'][0:5]:
    if (feature['geometry']['type'] == 'LineString'):
        print feature
        print feature['geometry']['coordinates']
        print feature['properties']['attractivity']

# z coordinates ziskej prvni a posledni, ale nech si i vsechny uvnitr
# z properties si nech jen score

print ""
print "EXAMPLE>>>>"
coordinates = [[14.434785, 50.07245], [14.43483, 50.072355], [14.434911, 50.072172], [14.435005, 50.071999], [14.435086, 50.071816], [14.43518, 50.071643], [14.435258, 50.071453]]
Start = coordinates[0][:]
End = coordinates[-1][:]
Score = 26
SegmentId = 0

print Start
print End
Segment = GraphEdgeSegment(Start, End, Score, SegmentId)

Segment.displaySegment()