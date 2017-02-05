import numpy as np
from evaluation import *
from classification import *
from netrunner import *

#IMAGE_FOLDER = '/media/ekmek/Vitek/_ImageNetRelatedStuffs/test_data/'
IMAGE_FOLDER = '/media/ekmek/Vitek/_ImageNetRelatedStuffs/val_data/'

# prepare list of image names
from os import listdir
from os.path import isfile, join
FILE_NAMES = [IMAGE_FOLDER + f for f in listdir(IMAGE_FOLDER) if isfile(join(IMAGE_FOLDER, f))]

image_list = FILE_NAMES[0:50]
#image_list = FILE_NAMES
classification_file = 'classified.txt'
N = 5
topNerror = N

model_handler = netrunner()
#model_handler = []

# run classification on them
classification(image_list, classification_file, topNerror, model_handler )

#groundtruth_file = '/media/ekmek/Vitek/_ImageNetRelatedStuffs/ILSVRC2010_test_ground_truth.txt'
groundtruth_file = '/media/ekmek/Vitek/_ImageNetRelatedStuffs/ILSVRC2010_validation_ground_truth.txt'
# evaluate results
evaluation( groundtruth_file, classification_file, topNerror )

# (save the results to a log or smth.)
