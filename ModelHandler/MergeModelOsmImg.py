import DatasetHandler.CreateDataset as CreateDataset
from ModelHandler.ModelTester import load_features
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

# -------------------------------------------------------------------------------------------

from keras.layers import Dropout, Flatten
from keras.utils import plot_model
import numpy as np
from Downloader.VisualizeHistory import visualize_history

osm = np.asarray(osm)
osm_val = np.asarray(osm_val)

input_shape_osm = osm.shape[1:]
input_shape_img = train_data.shape[1:]
print input_shape_osm, input_shape_img

number_of_repeats = 3

from keras.models import Sequential, Model
from keras.layers import Concatenate, Dense, LSTM, Input, concatenate
osm_features_input = Input(shape=input_shape_osm)
osm_features = Dense(256, activation='relu')(osm_features_input)
osm_features = Dropout(0.5)(osm_features)

img_features_input = Input(shape=input_shape_img)
img_features = Flatten()(img_features_input)

top = concatenate([osm_features, img_features])
for i in range(0,number_of_repeats):
    top = Dense(256, activation='relu')(top)
    top = Dropout(0.5)(top)
top = Dense(1, activation='sigmoid')(top)

model = Model(inputs=[osm_features_input, img_features_input], outputs=top)
model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
plot_model(model, to_file='v1-250.png', show_shapes=True)

epochs = 250
history = model.fit([osm, train_data], train_labels,
              epochs=epochs, batch_size=32,
              validation_data=([osm_val, validation_data], validation_labels))
history = history.history

name = '/home/ekmek/Vitek/MGR-Project-Code/ModelHandler/concat-'+str(number_of_repeats)+"repeats"+str(epochs)+"epochs---v1-250"
visualize_history(history, show=True, save=True, save_path=name)
