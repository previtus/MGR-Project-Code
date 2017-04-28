import h5py
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense
import DatasetHandler.CreateDataset as CreateDataset
from Downloader.ImageHelpers import len_
from Downloader.VisualizeHistory import *

import os.path
import keras
import time
import os
print os.getcwd()
print "this one needs th to be set up in Defaults and in Keras.json"

# INPUTS
LocalFolder = '/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/ModelFiles/NVMTesting/'

vgg16_weights_path = '/home/ekmek/Desktop/Project II/vgg16_weights.h5'

target_folder = LocalFolder+'results/'
plus = '-nvm-testing-'
# SETTINGS
img_width, img_height = 150, 150
nb_epoch = 50


[dataset, uniqueId] = CreateDataset.load_8376_resized_150x150(desired_number=100, seed=42)
[x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)

import random
random.seed(None)

def save_bottlebeck_features(x, y, x_val, y_val):

    # VGG16 network
    model = Sequential()
    model.add(ZeroPadding2D((1, 1), input_shape=(3, img_width, img_height)))

    model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(64, 3, 3, activation='relu', name='conv1_2'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(128, 3, 3, activation='relu', name='conv2_2'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, 3, 3, activation='relu', name='conv3_3'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv4_3'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_1'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_2'))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(512, 3, 3, activation='relu', name='conv5_3'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    # manually load weights into the partial VGG16 model
    assert os.path.exists(vgg16_weights_path), 'VGG16 model weights not found!'
    f = h5py.File(vgg16_weights_path, mode="r")
    print f

    for k in range(f.attrs['nb_layers']):
        if k >= len(model.layers):
            # we don't look at the last (fully-connected) layers in the savefile
            break
        g = f['layer_{}'.format(k)]
        weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
        model.layers[k].set_weights(weights)
    f.close()
    print('VGG16 partial model loaded.')

    bottleneck_features_train = model.predict(x,verbose=1)
    np.save(open(target_folder+'features_train_VGG16manual'+plus+'.npy', 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict(x_val,verbose=1)
    np.save(open(target_folder+'features_validation_VGG16manual'+plus+'.npy', 'w'), bottleneck_features_validation)


def train_top_model(x, y, x_val, y_val):
    train_data = np.load(open(target_folder+'features_train_VGG16manual'+plus+'.npy'))
    train_labels = np.array(y)

    validation_data = np.load(open(target_folder+'features_validation_VGG16manual'+plus+'.npy'))
    validation_labels = np.array(y_val)

    print train_data.shape[1:]

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
    history = model.fit(train_data, train_labels,
              nb_epoch=nb_epoch, batch_size=32,
              validation_data=(validation_data, validation_labels))

    saveHistory(history.history, LocalFolder+'results/history_VGG16manual'+plus+'.npy')
    visualize_history(history.history, save=True, save_path=LocalFolder+'results/VGG16manual'+plus+'_'+str(nb_epoch))

#save_bottlebeck_features(x, y, x_val, y_val)
#train_top_model(x, y, x_val, y_val)
