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
for i in range(0, number_of_repeats - 1):
    top = Dense(256, activation='relu')(top)
    top = Dropout(0.5)(top)
output = Dense(1, activation='sigmoid')(top)

model = Model(inputs=osm_features_input, outputs=output)

model_settings = {}
model_settings["optimizer"] = 'rmsprop'
model_settings["loss_func"] = 'mean_squared_error'
model_settings["metrics"] = ['mean_absolute_error']
model_settings["loss_func"] = 'mean_absolute_error'
model_settings["metrics"] = ['mean_squared_error']
model_settings["epochs"] = 20

model.compile(optimizer=model_settings["optimizer"], loss=model_settings["loss_func"],
              metrics=model_settings["metrics"])

##
## Kerutils from https://github.com/samyzaf/kerutils
## somewhat edited for regression, loss minimation instead of accuracy maximalization
##

from kerutils import FitMonitor, show_scores
import kerutils
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
print("Train: metric=%f, loss=%f" % (metric, loss))
loss, metric = model.evaluate(X_test, Y_test, verbose=0)
print("Validation: metric=%f, loss=%f" % (metric, loss))

print '--------------------------'

show_scores(model, h, X_train, Y_train, X_test, Y_test)
