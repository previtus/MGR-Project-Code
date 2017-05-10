# Provides the rest of the ModelHandler code with models. Works with the lower level of code in /Create Model
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
import ModelHandler.CreateModel.KerasApplicationsModels as Models

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

def get_cnn_models(Settings):
    '''
    Loads the cnn part of models
    :param Settings:
    :return:
    '''
    models = []
    number_of_models = len(Settings["models"])
    print "## Loading",number_of_models,"models with their CNNs."

    for model in Settings["models"]:
        cnn_model = model["cnn_model"]
        model_cnn = Models.get_model(cnn_model)
        #DefaultModel["cut_cnn"]

        # More complicated models to be added

        if model["model_type"] is 'simple_cnn_with_top':
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
