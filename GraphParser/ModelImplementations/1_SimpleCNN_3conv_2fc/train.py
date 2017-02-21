'''
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
 --- taky facha, ale je potiz, ze pak ty obrazky jsou cilene divne :E
 --- mozna local_abs_dir = os.path.dirname(__file__) a od toho jet dal
'''

'''
import sys
sys.path.append('/home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser/')
import os
cwd = os.getcwd()
print cwd
# IDLE /home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser/ModelImplementations/1_SimpleCNN_3conv_2fc
# __name__> __main__
# __file__> /home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser/ModelImplementations/1_SimpleCNN_3conv_2fc/train.py

# PyCharm /home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser
# __name__> __main__
# __file__> /home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser/ModelImplementations/1_SimpleCNN_3conv_2fc/train.py

# MAYBE UNIFY WITH
#os.chdir(path) ("change the current working directory to path")

print __name__
print __file__
# V IDLE pak facha:
#plot(model, to_file='results/model.png', show_shapes=True)
exit()
'''

from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils.visualize_util import plot
import keras
import time
from KerasPreparation import *
from VisualizeHistory import *

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

LocalFolder = 'ModelImplementations/1_SimpleCNN_3conv_2fc/'
Folder = '1100downloaded_vII/'
segments_file = Folder+'SegmentsData.dump'
images_add = Folder

plot(model, to_file=LocalFolder+'results/model.png', show_shapes=True)

#[x, y, x_val, y_val] = Prepare_DataLabels(segments_file,300,300,path_to_images=images_add)
#[train_generator, validation_generator] = Prepare_DataLabels_generators(segments_file,150,150,path_to_images=images_add)
[x, y, x_val, y_val] = Prepare_DataLabels_withGeneratedData(segments_file,img_width, img_height,validation_split=0.25,path_to_images=Folder,shuffle_=False,seed_=42)

# s write_images=True zlobi
now = time.strftime("%c")
log1 = keras.callbacks.TensorBoard(log_dir=LocalFolder+'data/'+now, histogram_freq=1, write_graph=True, write_images=False)
log2 = keras.callbacks.CSVLogger(LocalFolder+'data/logCSV.csv', separator=',', append=False)
logcalls = [log1, log2]
#logcalls = []
'''
nb_train_samples = 2000
nb_validation_samples = 800
nb_epoch = 50
hi = model.fit_generator(
        train_generator,
        samples_per_epoch=nb_train_samples,
        nb_epoch=nb_epoch,
        validation_data=validation_generator,
        nb_val_samples=nb_validation_samples,
    )
'''
nb_epoch = 50
history = model.fit(x, np.array(y),
        nb_epoch=nb_epoch, batch_size=32,
        validation_data=(x_val, np.array(y_val)),
                    callbacks=logcalls)

model.save(LocalFolder+'data/pokusCNN_V2_s1000_e5.h5')

saveHistory(history.history, LocalFolder+'results/history.npy')
