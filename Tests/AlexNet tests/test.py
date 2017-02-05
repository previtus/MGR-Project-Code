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

#image_list = FILE_NAMES[0:100]
image_list = FILE_NAMES
output_file = '___nvm'
N = 10
topNerror = N

model_handler = netrunner()
#model_handler = []

# run classification on them
classifications = classification(image_list, output_file, topNerror, model_handler )
## print classifications
## ## save to file!

#groundtruth_file = '/media/ekmek/Vitek/_ImageNetRelatedStuffs/ILSVRC2010_test_ground_truth.txt'
groundtruth_file = '/media/ekmek/Vitek/_ImageNetRelatedStuffs/ILSVRC2010_validation_ground_truth.txt'
classification_file = '___nvm'
# evaluate results
evaluation( groundtruth_file, classifications, topNerror )

# (save the results to a log or smth.)