import os
import numpy as np

from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.utils import plot_model
from Downloader.VisualizeHistory import saveHistory, visualize_history

def doWeNeedToCook(filename_features_train, filename_features_test):
    return not(os.path.exists(filename_features_train) and os.path.getsize(filename_features_train) > 0
        and os.path.exists(filename_features_test) and os.path.getsize(filename_features_test) > 0)

def predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model):
    # dimensions of x are (num,3,x_dim, y_dim) = (75, 3, 150, 150)
    # VGG16 network
    bottleneck_features_train = model.predict(x,verbose=1)
    np.save(open(filename_features_train, 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict(x_val,verbose=1)
    np.save(open(filename_features_test, 'w'), bottleneck_features_validation)

def load_features(filename_features_train, filename_features_test, y, y_val):
    train_data = np.load(open(filename_features_train))
    train_labels = np.array(y)

    validation_data = np.load(open(filename_features_test))
    validation_labels = np.array(y_val)
    return [train_data, train_labels, validation_data, validation_labels]

def build_top_model(input_shape, number_of_repeats):
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    for i in range(0,number_of_repeats):
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

def train_top_model(model, train_data, train_labels, epochs, validation_data, validation_labels, save_img_name=None):

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
    if save_img_name is not None:
        plot_model(model, to_file=save_img_name+'.png', show_shapes=True)

    history = model.fit(train_data, train_labels,
              epochs=epochs, batch_size=32,
              validation_data=(validation_data, validation_labels))
    return history.history

def save_model_history(history, filename_history, filename_image):
    saveHistory(history, filename_history)
    visualize_history(history, show=False, save=True, save_path=filename_image)
