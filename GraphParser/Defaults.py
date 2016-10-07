# Defaults.py

### PreprocessData part ###

FromEdgeID = 0 # 2 -> will start with 002.jpg
ToEdgeID = 15 # 14 -> will end with 013.jpg
# out of 1165640!
PIXELS_X = 300
PIXELS_Y = 150
NUMBER_OF_ZEROS_PADDING = '03'

DOWNLOAD_TIMEOUT = 0.7

FILE_NOT_FOUND_CHECKSUM = "86f3a67162a58d4c1622ef9f9ea635e3"

EDGESFILES = r'../../graph/edges_.csv'
NODESFILES = r'../../graph/nodes_.csv'
DATASTRUCTUREFILE = 'SegmentsData.dump'

global ERROR_MESSAGE_NO_ERROR
global ERROR_MESSAGE_NOT_FOUND
global ERROR_MESSAGE_FAILED_MANY_TIMES
ERROR_MESSAGE_NO_ERROR = -1
ERROR_MESSAGE_NOT_FOUND = 404
ERROR_MESSAGE_FAILED_MANY_TIMES = 101


### Learning part ###

### Classification part ###
