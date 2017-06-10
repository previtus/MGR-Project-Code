import numpy as np
import copy

from keras.optimizers import SGD
from keras import backend as K
from resnet152keras import resnet152_model

def run_test():
    img_rows, img_cols = 299, 299 # Resolution of inputs
    channel = 3
    batch_size = 32
    nb_epoch = 50


    if K.image_dim_ordering() == 'th':
        # Use pre-trained weights for Theano backend
        weights_path = '/storage/brno2/home/previtus/MGR-Project-Code/Tests/ResNet152_tests/resnet152_weights_th.h5'
    else:
        # Use pre-trained weights for Tensorflow backend
        weights_path = '/storage/brno2/home/previtus/MGR-Project-Code/Tests/ResNet152_tests/resnet152_weights_tf.h5'

    # Test pretrained model
    model = resnet152_model(img_rows, img_cols, channel, weights_path, load_top=False, new_top=True)

    # LOCK LAYERS!
    for layer in model.layers[:10]:
        layer.trainable = False

    # lr 0.001
    sgd = SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='mean_squared_error', metrics=['mean_absolute_error'])

    model.summary()

    # data (InputLayer)                (None, 299, 299, 3)   0
    # ...
    # res5c_relu (Activation)          (None, 10, 10, 2048)  0
    # avg_pool (AveragePooling2D)      (None, 1, 1, 2048)    0
    # flatten_2 (Flatten)              (None, 2048)          0
    # fc8 (Dense)                      (None, 1)             2049

    from inits import get_dataset, len_
    dataset, osm, osm_val, y, y_val, x, x_val = get_dataset()

    # Now try this model on my current x,y

    history = model.fit(x, y,
              batch_size=batch_size,
              nb_epoch=nb_epoch,
              #shuffle=True,
              verbose=1,
              validation_data=(x_val, y_val),
    )

    from Downloader.VisualizeHistory import saveHistory
    from Downloader.VisualizeHistory import visualize_history

    path = '/storage/brno2/home/previtus/MGR-Project-Code/Tests/ResNet152_tests/'
    saveHistory(history.history, path+"history_1200x_markable_299x299_nonShuffle32batch.npy")

    custom_title = 'Resnet152_test_640_30m'
    visualize_history(history, show=False, save=True, save_path=path+'graph_1200x_markable_299x299_nonShuffle32batch.png', custom_title=custom_title)
