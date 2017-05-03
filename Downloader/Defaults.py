# Defaults.pyNODESFILES_GEOJSON = r'../../graph_new_data/attractivity_previtus_data_1_nodes.geojson'


### PreprocessData part ###

FromEdgeID = 0 # 2 -> will start with 002.jpg
ToEdgeID = 2 #15 # 14 -> will end with 013.jpg

#no data on:
#FromEdgeID = 5288
#ToEdgeID = 5300
# 1st dataset: out of 1165640! (there are 1165641 lines and the 1st one is just text)
# 2nd dataset: out of 5556 edges
PIXELS_X = 299
PIXELS_Y = 299
NUMBER_OF_ZEROS_PADDING = '04'

DOWNLOAD_TIMEOUT = 0.7

# False mostly!
DOWNLOAD_OVERRIDE_PRETEND_YOU_WERE_ABLE_TO_DOWNLOAD_ALL_BUT_DONT_DO_IT = False

#FILE_NOT_FOUND_CHECKSUM = "460cd333e543a08a47cb4b986de5942b" #300x300
#FILE_NOT_FOUND_CHECKSUM = "b31c4837d780bd4ea95da73ba0e8a54b" #150x150
FILE_NOT_FOUND_CHECKSUM = "79d895a10e5947aa682b79cf0cfdcda1" #640x640
#FILE_NOT_FOUND_CHECKSUM = "a1ffb93c541716d60f3536d3ed308339" #299x299

# TODO: add a test for a known 404 image with current px*py and md5
# /home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/1200x_markable_640x640/images/1189_0.jpg 79d895a10e5947aa682b79cf0cfdcda1 False
# No photographic information on the spot.
# ...... all the way to
#/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/1200x_markable_640x640/images/1199_4.jpg 79d895a10e5947aa682b79cf0cfdcda1 False
#No photographic information on the spot.


#QUOTA_EXCEEDED_CHECKSUM="62b6f414127ae3a630639c8572360dd7" #299x299 maybe

# two types of error images
QUOTA_EXCEEDED_CHECKSUM="3039500ea7b46f5f2e33f06b997b9bb8" #640x640
QUOTA_EXCEEDED_CHECKSUM_billing_msg="b2328ec7ff935944a85723daddf0e8b7" #640x640

BAD_MD5_LIST = [
    "460cd333e543a08a47cb4b986de5942b",
    "b31c4837d780bd4ea95da73ba0e8a54b",
    "79d895a10e5947aa682b79cf0cfdcda1",
    "a1ffb93c541716d60f3536d3ed308339",
    "62b6f414127ae3a630639c8572360dd7",
    "3039500ea7b46f5f2e33f06b997b9bb8",
    "b2328ec7ff935944a85723daddf0e8b7"
]

# TODO: Check for file not found in different manner
# probably: https://developers.google.com/maps/documentation/javascript/streetview#StreetViewService

EDGESFILES_GEOJSON = r'../../graph_new_data/attractivity_previtus_data_1_edges.geojson'
DATASTRUCTUREFILE = 'SegmentsData.dump'

global ERROR_MESSAGE_NO_ERROR
global ERROR_MESSAGE_NOT_FOUND
global ERROR_MESSAGE_FAILED_MANY_TIMES
global ERROR_MESSAGE_QUOTA
global ERROR_GENERAL
ERROR_MESSAGE_NO_ERROR = -1
ERROR_MESSAGE_NOT_FOUND = 404
ERROR_MESSAGE_FAILED_MANY_TIMES = 101
ERROR_MESSAGE_QUOTA = 333
ERROR_GENERAL = 1337

# OSM Formula version
OSM_MARKING_VERSION = '0.0c'

# KERAS SETTING
# tf example (40, 299, 299, 3)

# experiments worked with th
# new Keras version expects None (instead of 'default') to search for the default system set value
KERAS_SETTING_DIMENSIONS = 'channels_last'

### Learning part ###
# Number of epochs?, etc...

### Classification part ###
# Method of measuring distance between labels_from_segments <-> labels_from_model
