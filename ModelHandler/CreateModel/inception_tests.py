import keras.applications as applications
from keras.preprocessing import image
from keras.models import Model, Sequential
from keras.layers import Dense, Dropout, GlobalAveragePooling2D, Flatten
from keras import backend as K
import keras.utils.visualize_util as visualize_util
import numpy as np
import DatasetHandler.CreateDataset as CreateDataset
from Downloader.ImageHelpers import len_
from Downloader.VisualizeHistory import *

input_shape=(299, 299, 3)
base_model = applications.vgg16.VGG16(include_top=False, weights='imagenet', input_tensor=None, input_shape=input_shape)

#base_model = applications.inception_v3.InceptionV3(weights='imagenet', include_top=True, input_shape=input_shape)
#base_model = applications.xception.Xception(include_top=False, weights='imagenet', input_tensor=None, input_shape=input_shape)

#dataset = CreateDataset.load_3342_valid_images_299x299(desired_number=50, seed=42)
dataset = CreateDataset.load_8376_resized_299x299(desired_number=1200, seed=42)
[x, y, x_val, y_val] = dataset.getDataLabels_split()

print len_(x)
print len_(x_val)

target_folder = '../../Data/ModelFiles/'
bottleneck_features_train = base_model.predict(x, verbose=1)
np.save(open(target_folder + 'VGG16_299_features_train_1200.npy', 'w'), bottleneck_features_train)
bottleneck_features_validation = base_model.predict(x_val, verbose=1)
np.save(open(target_folder + 'VGG16_299_features_validation_1200.npy', 'w'), bottleneck_features_validation)

'''
train_data = np.load(open(target_folder + 'Xception_features_train_1200.npy'))
train_labels = np.array(y)

validation_data = np.load(open(target_folder + 'Xception_features_validation_1200.npy'))
validation_labels = np.array(y_val)

model = Sequential()
model.add(GlobalAveragePooling2D(input_shape=train_data.shape[1:]))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_squared_logarithmic_error'])

# ValueError: Input arrays should have the same number of samples as target arrays. Found 960 input samples and 1440 target samples.
# x je shape
# x_val je shape
print len_(y)
print len_(y_val)
print len_(train_labels)
print len_(validation_labels)

logcalls = []
nb_epoch = 50
history = model.fit(train_data, train_labels,
                    nb_epoch=nb_epoch, batch_size=32,
                    validation_data=(validation_data, validation_labels), callbacks=logcalls)

LocalFolder = '/home/ekmek/Project II/MGR-Project-Code/Data/ModelFiles/'
saveHistory(history.history, LocalFolder + 'results/history_withGlobAvgPool_with1200.npy')
visualize_history(history.history, save=True, save_path=LocalFolder + 'results/history_withGlobAvgPool_with1200_' + str(nb_epoch))
'''

'''
# Build custom top

x = base_model.output
x = GlobalAveragePooling2D()(x) # instead of Flatten?

x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)
output_score = Dense(1, activation='sigmoid')(x)

# this is the model we will train
model = Model(input=base_model.input, output=output_score)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='rmsprop', loss='mean_squared_error')
#model.compile(optimizer='adam', loss='mean_squared_error')

visualize_util.plot(model, to_file='TEST.png', show_shapes=True)

'''