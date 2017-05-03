import DatasetHandler.CreateDataset as CreateDataset
from ModelHandler.CreateModel.ModelsFunctions import load_features, build_top_model, train_top_model, save_model_history
from Downloader.ImageHelpers import len_


# image features file
img_features_train_file = '/home/ekmek/Vitek/Logs/shared/features_train_data299mark-full-seed42_resnet50.npy'
img_features_val_file = '/home/ekmek/Vitek/Logs/shared/features_validation_data299mark-full-seed42_resnet50.npy'
segments_file = ''

dataset = CreateDataset.load_1200x_marked_299x299(desired_number=None, seed=42)

[x, y, x_val, y_val, osm, osm_val] = dataset.getDataLabels_split_with_osm(validation_split=0.25)
print 'x', len_(x), 'y', len_(y), 'osm', len_(osm)

[train_data, train_labels, validation_data, validation_labels] = load_features(img_features_train_file, img_features_val_file, y, y_val)

print "input shape of features", len_(train_data), "and labels", len_(train_labels)



from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, BatchNormalization
from keras.utils import plot_model
import numpy as np
from Downloader.VisualizeHistory import visualize_history

osm = np.asarray(osm)
osm_val = np.asarray(osm_val)

input_shape = osm.shape[1:]
print input_shape

number_of_repeats = 3
osm_features = Sequential()
osm_features.add(Dense(256, activation='relu',input_shape=input_shape))
osm_features.add(Dropout(0.5))

for i in range(0,number_of_repeats-1):
    osm_features.add(Dense(256, activation='relu'))
    osm_features.add(Dropout(0.5))
osm_features.add(Dense(1, activation='sigmoid'))
osm_features.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])

plot_model(osm_features, to_file='-1---to-score.png', show_shapes=True)

img_features = build_top_model(train_data.shape[1:], 3)
img_features.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])

plot_model(img_features, to_file='-2---to-score.png', show_shapes=True)



epochs = 100
history = osm_features.fit(osm, train_labels,
              epochs=epochs, batch_size=32,
              validation_data=(osm_val, validation_labels))
history = history.history

name = '/home/ekmek/Vitek/MGR-Project-Code/ModelHandler/'+str(number_of_repeats)+"repeats"+str(epochs)+"epochs---waaaa"
visualize_history(history, show=True, save=True, save_path=name)

