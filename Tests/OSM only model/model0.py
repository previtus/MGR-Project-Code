import inits
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.models import Model
from keras.layers import Input, concatenate

dataset, osm, osm_val, y, y_val = inits.get_dataset()

input_shape = dataset.getShapeOfOsm()

number_of_repeats = 2
osm_features_input = Input(shape=input_shape)
top = Dense(256, activation='relu')(osm_features_input)
top = Dropout(0.5)(top)
top = Dense(256, activation='relu')(top)
top = Dropout(0.5)(top)
output = Dense(1, activation='sigmoid')(top)

model = Model(inputs=osm_features_input, outputs=output)

model_settings = {}
model_settings["optimizer"] = 'rmsprop'
model_settings["loss_func"] = 'mean_absolute_error' #mean_squared_error
model_settings["metrics"] = ['mean_absolute_error']
model_settings["epochs"] = 50

model.name = 'model0'
model.compile(optimizer=model_settings["optimizer"], loss=model_settings["loss_func"],
              metrics=model_settings["metrics"])

##
## Kerutils from https://github.com/samyzaf/kerutils
## somewhat edited for regression, loss minimation instead of accuracy maximalization
##

from kerutils import FitMonitor, show_scores
fmon = FitMonitor()
#fmon = FitMonitor(thresh=0.05, maxloss=0.05, filename="model0_autosave.h5")

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
# Heavily overfits
#
'''
min_loss = 0.070534  epoch = 19
min_val_loss = 0.117932  epoch = 1
--------------------------
Train: metric mean_absolute_error=0.194500, loss=0.062831
Validation: metric mean_absolute_error=0.292885, loss=0.128716
'''

# mean_absolute_error
'''
min_loss = 0.204694  epoch = 48
min_val_loss = 0.299948  epoch = 46
--------------------------
Train: metric mean_absolute_error=0.191815, loss=0.191815
Validation: metric mean_absolute_error=0.310030, loss=0.310030

'''