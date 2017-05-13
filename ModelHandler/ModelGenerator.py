# Provides the rest of the ModelHandler code with models. Works with the lower level of code in /Create Model
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.models import Model
from keras.layers import Input, concatenate
import ModelHandler.CreateModel.KerasApplicationsModels as Models

from Omnipresent import len_

# Generate Model Parts
def build_simple_top_model(input_shape, number_of_repeats):
    '''
    Builds simple model of repeated FC blocks.
    :param input_shape: Keras needs to know the input shape.
    :param number_of_repeats: repeats of FC block additional to the first Flatten layer and the last sigmoid output layer.
    :return:
    '''
    model = Sequential()
    model.add(Flatten(input_shape=input_shape))
    for i in range(0,number_of_repeats):
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    return model

def build_osm_only_model(input_shape, number_of_repeats):
    '''
    Build a simple model with just OSM vector as it's input, couple of FC blocks and then sigmoid output of 1 score value
    :param input_shape:
    :param number_of_repeats:
    :return:
    '''
    osm_features_input = Input(shape=input_shape)
    top = Dense(256, activation='relu')(osm_features_input)
    top = Dropout(0.5)(top)
    for i in range(0,number_of_repeats-1):
        top = Dense(256, activation='relu')(top)
        top = Dropout(0.5)(top)
    output = Dense(1, activation='sigmoid')(top)

    model = Model(inputs=osm_features_input, outputs=output)
    return model

# Generate Whole Models
def get_top_models(models, datasets, Settings):
    '''
    Adds the right top models, now with proper knowledge of shapes of feature files.
    :param models:
    :param Settings:
    :return:
    '''
    number_of_models = len(Settings["models"])
    print "## Adding ",number_of_models," top models."

    index = 0
    for model_settings in Settings["models"]:
        # TODO: MODEL_TYPE_SPLIT

        if model_settings["model_type"] is 'simple_cnn_with_top':
            filename_features_train = model_settings["filename_features_train"]
            model = models[index]

            from ModelHandler.ModelTester import load_feature_file
            train_data = load_feature_file(filename_features_train)
            input_shape = train_data.shape[1:]
            model[1] = build_simple_top_model(input_shape=input_shape, number_of_repeats=model_settings["top_repeat_FC_block"])
            print model_settings["unique_id"], model

        elif model_settings["model_type"] is 'osm_only':
            model = models[index]

            dataset = datasets[ model_settings["dataset_pointer"] ]

            if not dataset.has_osm_loaded:
                print "For this model type, we need OSM vectors, choose dataset accordingly."
                Settings["interrupt"] = True
                return None

            input_shape = dataset.getShapeOfOsm()

            model[0] = build_osm_only_model(input_shape=input_shape, number_of_repeats=model_settings["top_repeat_FC_block"])
            print model_settings["unique_id"], model
        else:
            print "Yet to be programmed."

        index += 1
    return models

def get_cnn_models(Settings):
    '''
    Loads the cnn part of models
    :param Settings:
    :return:
    '''
    models = []
    number_of_models = len(Settings["models"])
    print "## Loading",number_of_models,"models with their CNNs."

    for model_settings in Settings["models"]:

        # TODO: MODEL_TYPE_SPLIT

        if model_settings["model_type"] is 'simple_cnn_with_top':
            cnn_model = model_settings["cnn_model"]
            model_cnn = Models.get_model(cnn_model)
            #DefaultModel["cut_cnn"]

            top = [] #build_top_model(input_shape=None, number_of_repeats=model["top_repeat_FC_block"])

            models.append([model_cnn, top])

        elif model_settings["model_type"] is 'osm_only':
            # No need to preload or cook features from images in this case
            osm_top = []
            models.append([osm_top])

        else:
            print "Yet to be programmed."

    return models
