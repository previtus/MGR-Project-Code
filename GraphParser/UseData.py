# UseData.py
from GenerateGIFAnimation import *
from Defaults import *
from preprocessdata import *

import pickle
import os

if not(os.path.isfile(DATASTRUCTUREFILE)):
    print "Data file was not found, downloading it!"
    PreprocessData(EDGESFILES, NODESFILES, DATASTRUCTUREFILE)

with open(DATASTRUCTUREFILE) as f:
    Segments = pickle.load(f)
    
    gifname = "".join(['animation_from_main_',str(FromEdgeID),'-',str(ToEdgeID),'.gif'])
    GenerateGIFAnimation(Segments, gifname)
