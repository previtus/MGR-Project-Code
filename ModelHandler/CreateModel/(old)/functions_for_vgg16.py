import DatasetHandler.CreateDataset as CreateDataset
from Downloader.ImageHelpers import len_
from Downloader.VisualizeHistory import visualize_history, saveHistory
from keras.utils import plot_model

from keras.applications.vgg16 import VGG16
import time
import datetime


import os.path
import os
print os.getcwd()
print "this one needs th to be set up in Defaults and in Keras.json"

from DatasetHandler.FileHelperFunc import use_path_which_exists

def train_top_model(x, y, x_val, y_val, filename_features_train, filename_features_test, filename_history, epochs):
    [train_data, train_labels, validation_data, validation_labels] = load_features(filename_features_train, filename_features_test, y, y_val)
    print train_data.shape[1:]

    model = build_top_model(train_data.shape[1:], 3)

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
    #plot_model(model, to_file='TEST.png', show_shapes=True)

    history = model.fit(train_data, train_labels,
              epochs=epochs, batch_size=32,
              validation_data=(validation_data, validation_labels))

    saveHistory(history.history, filename_history)
    visualize_history(history.history, show=False, save=True, save_path=filename_history+'_'+str(epochs))

def main_vgg16(name_of_the_experiment = '-nameMe', TMP_size_of_dataset=100, TMP_num_of_epochs = 1):
    # TMP_size_of_dataset influences save_bottlebeck_features
    # TMP_num_of_epochs influences train_top_model


    # INPUTS
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                   '/home/ekmek/Vitek/Logs/',
                     '/storage/brno2/home/previtus/Logs/']
    local_folder = use_path_which_exists(log_folders)
    print local_folder

    now = datetime.datetime.now()
    specific_folder_name = str(now.day) + 'th' + '-' + str(now.hour) + '-' + str(now.minute) + '_' + name_of_the_experiment # <day>th-hour-minute_experimentName
    target_folder = local_folder + specific_folder_name + '/'

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    if not os.path.exists(local_folder + 'shared/'):
        os.makedirs(local_folder + 'shared/')

    # SETTINGS

    dataset = CreateDataset.load_1200x_marked_299x299(desired_number=TMP_size_of_dataset, seed=42)
    [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)

    import random
    random.seed(None)

    print len_(x)

    uniqueId = dataset.unique_id

    filename_features_train = local_folder+'shared/'+'features_train_'+uniqueId+'.npy'
    filename_features_test = local_folder+'shared/'+'features_validation_'+uniqueId+'.npy'

    filename_history = target_folder + 'history_' + name_of_the_experiment + '.npy'

    if doWeNeedToCook(filename_features_train, filename_features_test):

        start = time.time()

        model = VGG16(weights='imagenet', include_top=False)
        print('VGG16 partial model loaded.')

        predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model)
        print "### 1st step TIME ", format(time.time() - start, '.2f'), " sec."
    else:
        print "### 1st step RECYCLED precomputed features"

    start = time.time()
    train_top_model(x, y, x_val, y_val, filename_features_train, filename_features_test, filename_history, TMP_num_of_epochs)
    print "### 2nd step TIME ", format(time.time() - start, '.2f'), " sec."

import sys
import time

from ModelHandler.CreateModel.functions_for_vgg16 import *

# DEFAULT VALUES:
TMP_size_of_dataset=5
TMP_num_of_epochs=1
name_of_the_experiment = '-test'

# python python_script.py var1 var2 var3
if len(sys.argv) > 3:
    TMP_size_of_dataset = int(sys.argv[1])  # var1
    TMP_num_of_epochs = int(sys.argv[2])  # var2
    name_of_the_experiment = sys.argv[3]  # var3
else:
    print "Using default values. Please run as: python_script.py sizeOfDataset numOfEpochs nameOfExp"

print "[Setting] python_script.py", TMP_size_of_dataset, TMP_num_of_epochs, name_of_the_experiment


#d = load_8376_resized_150x150(desired_number=10)
#d.statistics()

start = time.time()
print time.ctime()

main_vgg16(TMP_size_of_dataset=TMP_size_of_dataset, TMP_num_of_epochs=TMP_num_of_epochs, name_of_the_experiment = name_of_the_experiment)

end = time.time()
print time.ctime()

print "### TOTAL TIME ", format(end - start, '.2f'), " sec."
