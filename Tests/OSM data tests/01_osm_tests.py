from osmread import parse_file, Way


path_to_pbf_file = "small_planet_14.43,50.062_14.485,50.086.osm.pbf"
print path_to_pbf_file

# SLOWER
'''
highway_count = 0
for entity in parse_file(path_to_pbf_file):
    if isinstance(entity, Way) and 'highway' in entity.tags:
        highway_count += 1

print("%d highways found" % highway_count)
# 4921 highways found
'''

# FASTER
from imposm.parser import OSMParser

# simple class that handles the parsed OSM data.
class HighwayCounter(object):
    highways = 0

    def ways(self, ways):
        # callback method for ways
        for osmid, tags, refs in ways:
            if 'highway' in tags:
              self.highways += 1

# instantiate counter and parser and start parsing
counter = HighwayCounter()
p = OSMParser(concurrency=4, ways_callback=counter.ways)
p.parse(path_to_pbf_file)

# done
print counter.highways

