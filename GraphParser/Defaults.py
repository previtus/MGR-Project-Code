# Defaults.py

### PreprocessData part ###

FromEdgeID = 0 # 2 -> will start with 002.jpg
ToEdgeID = 5500 #15 # 14 -> will end with 013.jpg
# 1st dataset: out of 1165640! (there are 1165641 lines and the 1st one is just text)
# 2nd dataset: out of 5556 edges
PIXELS_X = 150
PIXELS_Y = 150
NUMBER_OF_ZEROS_PADDING = '03'

DOWNLOAD_TIMEOUT = 0.7

FILE_NOT_FOUND_CHECKSUM = "460cd333e543a08a47cb4b986de5942b" #300x300
FILE_NOT_FOUND_CHECKSUM = "b31c4837d780bd4ea95da73ba0e8a54b" #150x150
# TODO: Check for file not found in different manner
# probably: https://developers.google.com/maps/documentation/javascript/streetview#StreetViewService

EDGESFILES = r'../../graph/edges_.csv'
NODESFILES = r'../../graph/nodes_.csv'
EDGESFILES_GEOJSON = r'../../graph_new_data/attractivity_previtus_data_1_edges.geojson'
NODESFILES_GEOJSON = r'../../graph_new_data/attractivity_previtus_data_1_nodes.geojson'
DATASTRUCTUREFILE = 'SegmentsData.dump'

global ERROR_MESSAGE_NO_ERROR
global ERROR_MESSAGE_NOT_FOUND
global ERROR_MESSAGE_FAILED_MANY_TIMES
ERROR_MESSAGE_NO_ERROR = -1
ERROR_MESSAGE_NOT_FOUND = 404
ERROR_MESSAGE_FAILED_MANY_TIMES = 101


### Learning part ###
# Number of epochs?, etc...

### Classification part ###
# Method of measuring distance between labels_from_segments <-> labels_from_model