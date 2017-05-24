import inits
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, LeakyReLU, Convolution1D
from keras.layers.advanced_activations import PReLU, ELU, LeakyReLU, ThresholdedReLU
from keras.models import Model
from keras.layers import Input, concatenate

from keras_contrib.layers.advanced_activations import SReLU

dataset, osm, osm_val, y, y_val = inits.get_dataset()

input_shape = dataset.getShapeOfOsm()

osm_features_input = Input(shape=input_shape)
top = Dense(8, activation='relu')(osm_features_input)
#top = Dense(32)(osm_features_input)
#top = SReLU()(top)
top = Dropout(0.5)(top)

top = Dense(4, activation='relu')(osm_features_input)
#top = Dense(32)(osm_features_input)
#top = SReLU()(top)
top = Dropout(0.5)(top)

top = Dense(4, activation='relu')(osm_features_input)
top = Dropout(0.5)(top)

output = Dense(1, activation='sigmoid')(top)

model = Model(inputs=osm_features_input, outputs=output)

model_settings = {}
model_settings["optimizer"] = 'rmsprop'
model_settings["loss_func"] = 'mean_absolute_error' #mean_squared_error
model_settings["metrics"] = ['mean_absolute_error']
model_settings["epochs"] = 200

model.name = 'model1'
model.compile(optimizer=model_settings["optimizer"], loss=model_settings["loss_func"],
              metrics=model_settings["metrics"])

##
## Kerutils from https://github.com/samyzaf/kerutils
## somewhat edited for regression, loss minimation instead of accuracy maximalization
##

from kerutils import FitMonitor, show_scores
fmon = FitMonitor()
#fmon = FitMonitor(thresh=0.05, maxloss=0.05, filename="model1_autosave.h5")

X_train = osm
Y_train = y
X_test = osm_val
Y_test = y_val
h = model.fit(osm, y,
                    epochs=model_settings["epochs"], batch_size=32,
                    validation_data=(osm_val, y_val), verbose=0,
                    callbacks=[fmon])

# Evaluation
print '--------------------------'

loss, metric = model.evaluate(X_train, Y_train, verbose=0)
print("Train: metric mean_absolute_error=%f, loss=%f" % (metric, loss))
loss, metric = model.evaluate(X_test, Y_test, verbose=0)
print("Validation: metric mean_absolute_error=%f, loss=%f" % (metric, loss))

print '--------------------------'

show_scores(model, h, X_train, Y_train, X_test, Y_test)

#
#
#
'''
min_loss = 0.083832  epoch = 19
min_val_loss = 0.105901  epoch = 0
--------------------------
Train: metric mean_absolute_error=0.229479, loss=0.076965
Validation: metric mean_absolute_error=0.286389, loss=0.119701

'''

# mean_absolute_error
'''
min_loss = 0.240779  epoch = 94
min_val_loss = 0.275416  epoch = 73
--------------------------
Train: metric mean_absolute_error=0.228147, loss=0.228147
Validation: metric mean_absolute_error=0.288617, loss=0.288617
'''