import h5py
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Dropout, Flatten, Dense
import DatasetHandler.CreateDataset as CreateDataset
from Downloader.ImageHelpers import len_
from Downloader.VisualizeHistory import *

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
import time

import os.path
import os
print os.getcwd()
print "this one needs th to be set up in Defaults and in Keras.json"

from DatasetHandler.FileHelperFunc import use_path_which_exists

def save_bottlebeck_features(x, y, x_val, y_val, filename_features_train, filename_features_test):
    # dimensions of x are (num,3,x_dim, y_dim) = (75, 3, 150, 150)
    img_width = len_(x)[2]
    img_height = len_(x)[3]

    # VGG16 network
    model = VGG16(weights='imagenet', include_top=False)
    print('VGG16 partial model loaded.')

    bottleneck_features_train = model.predict(x,verbose=1)
    np.save(open(filename_features_train, 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict(x_val,verbose=1)
    np.save(open(filename_features_test, 'w'), bottleneck_features_validation)


def train_top_model(x, y, x_val, y_val, filename_features_train, filename_features_test, filename_history, epochs):

    train_data = np.load(open(filename_features_train))
    train_labels = np.array(y)

    validation_data = np.load(open(filename_features_test))
    validation_labels = np.array(y_val)

    print train_data.shape[1:]

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
    history = model.fit(train_data, train_labels,
              epochs=epochs, batch_size=32,
              validation_data=(validation_data, validation_labels))

    saveHistory(history.history, filename_history)
    visualize_history(history.history, show=False, save=True, save_path=filename_history+'_'+str(epochs))

def main_vgg16(name_of_the_experiment = '-nameMe', TMP_size_of_dataset=100, TMP_num_of_epochs = 1):
    # TMP_size_of_dataset influences save_bottlebeck_features
    # TMP_num_of_epochs influences train_top_model


    # INPUTS
    local_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/ModelFiles/', '/storage/brno2/home/previtus/MGR-Project-Code/Data/ModelFiles/']
    local_folder = use_path_which_exists(local_folders)

    local_folder = local_folder+'NVMTesting/'

    vgg16_locations = ['/home/ekmek/Desktop/Project II/vgg16_weights.h5', '/storage/brno2/home/previtus/vgg16_weights.h5']
    vgg16_weights_path = use_path_which_exists(vgg16_locations)

    target_folder = local_folder + 'results/'

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # SETTINGS

    [dataset, uniqueId] = CreateDataset.load_8376_resized_150x150(desired_number=TMP_size_of_dataset, seed=42)
    [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)

    import random
    random.seed(None)

    print len_(x)

    filename_features_train = target_folder+'features_train_VGG16manual'+name_of_the_experiment+'.npy'
    filename_features_test = target_folder+'features_validation_VGG16manual'+name_of_the_experiment+'.npy'
    filename_history = target_folder + 'history_VGG16manual' + name_of_the_experiment + '.npy'

    start = time.time()
    save_bottlebeck_features(x, y, x_val, y_val, filename_features_train, filename_features_test)
    print "### 1st step TIME ", format(time.time() - start, '.2f'), " sec."
    start = time.time()

    train_top_model(x, y, x_val, y_val, filename_features_train, filename_features_test, filename_history, TMP_num_of_epochs)
    print "### 2nd step TIME ", format(time.time() - start, '.2f'), " sec."
