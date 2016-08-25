import csv
from fce01c_csv_load_segment_by_ids import loadSegment

csv_file = open(r'edges_small.csv')
reader = csv.reader(csv_file, skipinitialspace=True)
header = reader.next()
print header

random_segment = reader.next() # first line
print random_segment

FromId = random_segment[0]
ToId = random_segment[1]
Popularity = random_segment[4]

Segment = loadSegment(FromId, ToId)
print "from"
print Segment[0][0]
print Segment[0][2]
print "to"
print Segment[1][0]
print Segment[1][2]

api = open('../apicode.txt', 'r').read()
#print api

url1 = ["http://maps.googleapis.com/maps/api/streetview?size=600x400&location=",Segment[0][0],",",Segment[0][2],"&heading=151.78&key=", api]
url2 = ["http://maps.googleapis.com/maps/api/streetview?size=600x400&location=",Segment[1][0],",",Segment[1][2],"&heading=151.78&key=", api]

print "".join(url1)
print "".join(url2)

import urllib
urllib.urlretrieve("".join(url1), "A.jpg")
urllib.urlretrieve("".join(url2), "B.jpg")

