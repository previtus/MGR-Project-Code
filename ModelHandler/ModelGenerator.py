# Provides the rest of the ModelHandler code with models. Works with the lower level of code in /Create Model
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
import ModelHandler.CreateModel.KerasApplicationsModels

# Generate Model Parts
def build_top_model(input_shape, number_of_repeats):
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    for i in range(0,number_of_repeats):
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Generate Whole Models
def get_model(name):
    return ModelHandler.CreateModel.KerasApplicationsModels.get_model(name)
