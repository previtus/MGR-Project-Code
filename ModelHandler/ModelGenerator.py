# Provides the rest of the ModelHandler code with models. Works with the lower level of code in /Create Model
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
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

# Generate Whole Models
def get_top_models(models, Settings):
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
        # More complicated models to be added

        if model_settings["model_type"] is 'simple_cnn_with_top':
            filename_features_train = model_settings["filename_features_train"]
            model = models[index]

            from ModelHandler.ModelTester import load_feature_file
            train_data = load_feature_file(filename_features_train)
            input_shape = train_data.shape[1:]
            model[1] = build_simple_top_model(input_shape=input_shape, number_of_repeats=model_settings["top_repeat_FC_block"])
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
        cnn_model = model_settings["cnn_model"]
        model_cnn = Models.get_model(cnn_model)
        #DefaultModel["cut_cnn"]

        # More complicated models to be added

        if model_settings["model_type"] is 'simple_cnn_with_top':
            top = [] #build_top_model(input_shape=None, number_of_repeats=model["top_repeat_FC_block"])

            models.append([model_cnn, top])
        else:
            print "Yet to be programmed."

    return models

    ''' ps settings has there params:
    DefaultModel = {}
    DefaultModel["unique_id"] = 'resnet50_top3FC_top150ep_10imgs_299px'
    DefaultModel["cnn_model"] = 'resnet50'
    DefaultModel["cut_cnn"] = 0
    DefaultModel["model_type"] = 'simple_cnn_with_top'
    DefaultModel["top_repeat_FC_block"] = 3
    DefaultModel["save_visualization"] = True

    # Train and Test specifics
    DefaultModel["epochs"] = 150
    DefaultModel["train_top"] = True
    DefaultModel["finetune_cnn"] = False
    DefaultModel["finetune_cnn_last"] = 10
    DefaultModel["finetune_all"] = False
    DefaultModel["finetune_all_last"] = 10

    '''
