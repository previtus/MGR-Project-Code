import inits
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, LeakyReLU, Convolution1D, BatchNormalization
from keras.layers.advanced_activations import PReLU, ELU, LeakyReLU, ThresholdedReLU
from keras.models import Model
from keras.layers import Input, concatenate

dataset, osm, osm_val, y, y_val = inits.get_dataset()

input_shape = dataset.getShapeOfOsm()

osm_features_input = Input(shape=input_shape)
top = BatchNormalization()(osm_features_input)

top = Dense(8, activation='relu')(top)
top = BatchNormalization()(top)
top = Dropout(0.5)(top)

top = Dense(4, activation='relu')(top)
top = BatchNormalization()(top)
top = Dropout(0.5)(top)

top = Dense(4, activation='relu')(top)
top = BatchNormalization()(top)
top = Dropout(0.5)(top)

top = Dense(2, activation='relu')(top)
top = BatchNormalization()(top)
top = Dropout(0.5)(top)

output = Dense(1, activation='sigmoid')(top)

model = Model(inputs=osm_features_input, outputs=output)

model_settings = {}
model_settings["optimizer"] = 'rmsprop'
model_settings["loss_func"] = 'mean_absolute_error' #mean_squared_error
model_settings["metrics"] = ['mean_absolute_error']
model_settings["epochs"] = 400

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

# mean_absolute_error
'''
min_loss = 0.265693  epoch = 378
min_val_loss = 0.276488  epoch = 235
--------------------------
Train: metric mean_absolute_error=0.243317, loss=0.243317
Validation: metric mean_absolute_error=0.290595, loss=0.290595
'''
