from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils.visualize_util import plot
import keras
from KerasPreparation import *

img_width, img_height = 150, 150

# 3 CONV
model = Sequential()
model.add(Convolution2D(32, 3, 3, input_shape=(3, img_width, img_height)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, 3, 3))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# 2 FC
model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# About custom loss function -> https://github.com/fchollet/keras/issues/4292
# (combination of multiple scores, plus of ssim)
# Article: "Loss Functions for Neural Networks for Image Processing" - https://arxiv.org/pdf/1511.08861v2.pdf
model.compile(loss='mean_squared_error',
              optimizer='rmsprop', # pry dobry pro recurrent neural networks
              metrics=['mean_squared_logarithmic_error']) #metrics=['accuracy'] mozna je accuracy zbytecna - jiny zpusob mereni skore (ps jde i top-5 err, tu ale k nicemu)

# PS> metrics jsou uzity pouze na vypis - ridi se to "loss" (ktera je ted mean_squared_error)
# ? Adam - http://arxiv.org/abs/1412.6980v8
# SDG
# ...

# TODO: Pridat moznost ze kdyz dokonverguje a moc se nemeni, aby se zastavilo ---- !
# ps> callback ModelCheckpoint = Save the model after every epoch.

plot(model, to_file='model.png', show_shapes=True)

segments_file = '1200downloaded/SegmentsData.dump'
images_add = '1200downloaded/'
#[x, y, x_val, y_val] = Prepare_DataLabels(segments_file,300,300,path_to_images=images_add)
[train_generator, validation_generator] = Prepare_DataLabels_generators(segments_file,150,150,path_to_images=images_add)

# s write_images=True zlobi
log1 = keras.callbacks.TensorBoard(log_dir='/home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser/1200downloaded', histogram_freq=1, write_graph=True, write_images=False)
log2 = keras.callbacks.CSVLogger('/home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser/1200downloaded/logCSV.csv', separator=',', append=False)
logcalls = [log1, log2]
#logcalls = []

nb_train_samples = 2000
nb_validation_samples = 400
nb_epoch = 50

model.fit_generator(
        train_generator,
        samples_per_epoch=nb_train_samples,
        nb_epoch=nb_epoch,
        validation_data=validation_generator,
        nb_val_samples=nb_validation_samples,
    callbacks=logcalls)

model.save('pokusCNN_s1000_e50.h5')

# History = model.fit(...)