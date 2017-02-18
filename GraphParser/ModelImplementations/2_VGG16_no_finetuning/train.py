# What happens here?
# we follow: https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html

import os
import h5py
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense

from VisualizeHistory import *
from KerasPreparation import *

# INPUTS
LocalFolder = 'ModelImplementations/2_VGG16_no_finetuning/'

vgg16_weights_path = '/home/ekmek/TEMP_SPACE/vgg16/vgg16_weights.h5'
Folder = '1100downloaded_vII/'
path_to_segments_file = Folder+'SegmentsData.dump'

# OUTPUTS
target_folder = LocalFolder+'data/'

# SETTINGS
img_width, img_height = 150, 150
nb_epoch = 50

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
    np.save(open(target_folder+'features_train.npy', 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict(x_val,verbose=1)
    np.save(open(target_folder+'features_validation.npy', 'w'), bottleneck_features_validation)


def train_top_model(x, y, x_val, y_val):
    train_data = np.load(open(target_folder+'features_train.npy'))
    train_labels = np.array(y)

    validation_data = np.load(open(target_folder+'features_validation.npy'))
    validation_labels = np.array(y_val)

    print train_data.shape[1:]

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_squared_logarithmic_error'])

    history = model.fit(train_data, train_labels,
              nb_epoch=nb_epoch, batch_size=32,
              validation_data=(validation_data, validation_labels))

    model.save_weights(target_folder + 'top_model_weights.h5')
    model.save(target_folder + 'top_model_whole.h5')

    saveHistory(history.history, LocalFolder+'results/history.npy')
    visualize_history(history.history,save=True, save_path=LocalFolder+'results/'+nb_epoch)


#[x, y, x_val, y_val] = Prepare_DataLabels(path_to_segments_file,150,150,path_to_images=Folder)
[x, y, x_val, y_val] = Prepare_DataLabels_withGeneratedData(path_to_segments_file,img_width, img_height,validation_split=0.25,path_to_images=Folder,shuffle_=False)
# PS: This is not really effective. We generate 2000+500 imgs and hold them somewhere in memory.
#     Better would be to make use of generators - and initiate them in both the same way in the two functions (with Shuffle=False)

'''
print type(x)
print type(y)
print type(x_val)
print type(y_val)

print len_(x)
print len_(y)
print len_(x_val)
print len_(y_val)
'''

#save_bottlebeck_features(x, y, x_val, y_val)
train_top_model(x, y, x_val, y_val)
