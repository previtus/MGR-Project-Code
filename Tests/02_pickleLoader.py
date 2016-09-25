from GenerateGIFAnimation import *
import pickle
import os

with open('../GraphParser/test_out.dump') as f:
    Segments = pickle.load(f)
    os.chdir('../GraphParser')
    GenerateGIFAnimation(Segments, 'test.gif')
