import os
import h5py
import numpy as np
from keras import optimizers
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers import Activation, Dropout, Flatten, Dense

from keras.utils.visualize_util import plot


def load_vgg16_model_with_custom_top(path_to_custom_top):

    # path to the model weights files.
    vgg16_weights_path = '/home/ekmek/TEMP_SPACE/vgg16/vgg16_weights.h5'
    img_width, img_height = 150, 150

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

    loading_method = 0

    if loading_method == 1:
        # PS: I am not sure, if this manual loading works the same

        model.add(Flatten(input_shape=model.output_shape[1:],name="fc_1"))
        model.add(Dense(256, activation='relu',name="fc_2"))
        model.add(Dropout(0.5,name="fc_3"))
        model.add(Dense(1, activation='sigmoid',name="fc_4"))
        assert os.path.exists(path_to_custom_top), 'Custom top weights not found!'
        f = h5py.File(path_to_custom_top)
        flatten_layer = model.layers[-4]
        flatten_dense1 = model.layers[-3]
        flatten_dropout = model.layers[-2]
        flatten_dense2 = model.layers[-1]

        t = [f['dense_1']['dense_1_W:0'], f['dense_1']['dense_1_b:0']]
        flatten_dense1.set_weights(t)
        t = [f['dense_2']['dense_2_W:0'], f['dense_2']['dense_2_b:0']]
        flatten_dense2.set_weights(t)

        f.close()
    elif loading_method == 0:
        top_model = Sequential()
        top_model.add(Flatten(input_shape=model.output_shape[1:],name="fc_1"))
        top_model.add(Dense(256, activation='relu',name="fc_2"))
        top_model.add(Dropout(0.5,name="fc_3"))
        top_model.add(Dense(1, activation='sigmoid',name="fc_4"))

        top_model.load_weights(path_to_custom_top)

        # join the models
        model.add(top_model)
        plot(top_model, to_file='results/img__top.png', show_shapes=True)
        print('Custom top loaded.')


    # set the first 25 layers (up to the last conv block)
    # to non-trainable (weights will not be updated)
    for layer in model.layers[:25]:
        layer.trainable = False

    model.compile(loss='mean_squared_error',
                  optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
                  metrics=[
                      'mean_squared_logarithmic_error'])  # metrics=['accuracy'] mozna je accuracy zbytecna - jiny zpusob mereni skore (ps jde i top-5 err, tu ale k nicemu)

    plot(model, to_file='results/img__vgg_with_custom_top.png', show_shapes=True)


    return model