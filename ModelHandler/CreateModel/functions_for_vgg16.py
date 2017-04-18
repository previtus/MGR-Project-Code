import h5py
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Dropout, Flatten, Dense
import DatasetHandler.CreateDataset as CreateDataset
from Downloader.ImageHelpers import len_
from Downloader.VisualizeHistory import *

import os.path
import os
print os.getcwd()
print "this one needs th to be set up in Defaults and in Keras.json"

from DatasetHandler.FileHelperFunc import use_path_which_exists

def save_bottlebeck_features(x, y, x_val, y_val, target_folder, name_of_the_experiment, vgg16_weights_path='vgg16_weights.h5'):
    # dimensions of x are (num,3,x_dim, y_dim) = (75, 3, 150, 150)
    img_width = len_(x)[2]
    img_height = len_(x)[3]

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
    f = h5py.File(vgg16_weights_path)
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
    np.save(open(target_folder+'features_train_VGG16manual'+name_of_the_experiment+'.npy', 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict(x_val,verbose=1)
    np.save(open(target_folder+'features_validation_VGG16manual'+name_of_the_experiment+'.npy', 'w'), bottleneck_features_validation)


def train_top_model(x, y, x_val, y_val, target_folder, name_of_the_experiment, nb_epoch):

    train_data = np.load(open(target_folder+'features_train_VGG16manual'+name_of_the_experiment+'.npy'))
    train_labels = np.array(y)

    validation_data = np.load(open(target_folder+'features_validation_VGG16manual'+name_of_the_experiment+'.npy'))
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

    saveHistory(history.history, target_folder+'history_VGG16manual'+name_of_the_experiment+'.npy')
    visualize_history(history.history, save=True, save_path=target_folder+'VGG16manual'+name_of_the_experiment+'_'+str(nb_epoch))

def main_vgg16():
    # INPUTS
    local_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/ModelFiles/', '/storage/brno2/home/previtus/MGR-Project-Code/Data/ModelFiles/']
    local_folder = use_path_which_exists(local_folders)

    local_folder = local_folder+'NVMTesting/'

    vgg16_locations = ['/home/ekmek/Desktop/Project II/vgg16_weights.h5', '/storage/brno2/home/previtus/vgg16_weights.h5']
    vgg16_weights_path = use_path_which_exists(vgg16_locations)

    target_folder = local_folder + 'results/'
    name_of_the_experiment = '-first_experiments'
    # SETTINGS
    nb_epoch = 1

    dataset = CreateDataset.load_8376_resized_150x150(desired_number=100, seed=42)
    [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)

    import random
    random.seed(None)

    save_bottlebeck_features(x, y, x_val, y_val, target_folder, name_of_the_experiment, vgg16_weights_path)
    train_top_model(x, y, x_val, y_val)