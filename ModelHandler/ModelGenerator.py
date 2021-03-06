# Provides the rest of the ModelHandler code with models. Works with the lower level of code in /Create Model
from keras.layers import Dropout, Flatten, Dense, Conv2D, MaxPooling2D
from keras.models import Model
from keras.layers import Input, concatenate, GlobalAveragePooling2D
import ModelHandler.CreateModel.KerasApplicationsModels as Models

from Omnipresent import len_

# Generate Model Parts
def build_img_only_top_model(input_shape, number_of_repeats):
    '''
    Builds simple model of repeated FC blocks.
    :param input_shape: Keras needs to know the input shape.
    :param number_of_repeats: repeats of FC block additional to the first Flatten layer and the last sigmoid output layer.
    :return:
    '''

    img_features_input = Input(shape=input_shape)
    top = Flatten()(img_features_input)
    for i in range(0,number_of_repeats):
        top = Dense(256, activation='relu')(top)
        top = Dropout(0.5)(top)
    output = Dense(1, activation='sigmoid')(top)

    model = Model(inputs=img_features_input, outputs=output)
    return model

def build_osm_only_model(input_shape, number_of_repeats, manual_width=256):
    '''
    Build a simple model with just OSM vector as it's input, couple of FC blocks and then sigmoid output of 1 score value
    :param input_shape: Keras needs to know the input shape.
    :param number_of_repeats: repeats of FC block additional to the first Flatten layer and the last sigmoid output layer.
    :param manual_width: manual width of the fc layers
    :return:
    '''
    osm_features_input = Input(shape=input_shape)
    top = Dense(manual_width, activation='relu')(osm_features_input)
    top = Dropout(0.5)(top)
    for i in range(0,number_of_repeats-1):
        top = Dense(manual_width, activation='relu')(top)
        top = Dropout(0.5)(top)
    output = Dense(1, activation='sigmoid')(top)

    model = Model(inputs=osm_features_input, outputs=output)
    return model

def build_img_osm_mix_model(input_shape_img, input_shape_osm, number_of_repeats):
    '''
    Build a combined model using both imgs and osm data.
    :param input_shape_img: Keras needs to know the input shapes for imgs.
    :param input_shape_osm: Keras needs to know the input shapes for osm vectors.
    :param number_of_repeats: repeats of FC block additional to the first Flatten layer and the last sigmoid output layer.
    :return:
    '''

    osm_features_input = Input(shape=input_shape_osm)
    osm_features = Dense(256, activation='relu')(osm_features_input)
    osm_features = Dropout(0.5)(osm_features)

    img_features_input = Input(shape=input_shape_img)
    img_features = Flatten()(img_features_input)

    top = concatenate([osm_features, img_features])
    for i in range(0,number_of_repeats):
        top = Dense(256, activation='relu')(top)
        top = Dropout(0.5)(top)
    top = Dense(1, activation='sigmoid')(top)

    model = Model(inputs=[osm_features_input, img_features_input], outputs=top)
    return model

def build_img_osm_mix_model_custom_base_cnn_top(input_shape_img, input_shape_osm, number_of_repeats):
    # Special case
    # Special case scenario where we are testing different base CNN which produce large features
    # Here we tested if using couple of Pooling and Convolutional layers before the input would help.
    osm_features_input = Input(shape=input_shape_osm)
    osm_features = Dense(256, activation='relu')(osm_features_input)
    osm_features = Dropout(0.5)(osm_features)

    img_features_input = Input(shape=input_shape_img)

    img_features = GlobalAveragePooling2D()(img_features_input)

    '''
    img_features = Conv2D(64, 3, padding='same', name='conv_topm_1')(img_features)
    img_features = Dropout(0.5)(img_features)
    img_features = MaxPooling2D(pool_size=(4, 4))(img_features)
    img_features = Dropout(0.5)(img_features)
    img_features = Conv2D(64, 3, padding='same', name='conv_topm_2')(img_features)
    img_features = Dropout(0.5)(img_features)
    img_features = MaxPooling2D(pool_size=(2, 2))(img_features)
    img_features = Dropout(0.5)(img_features)
    '''

    img_features = Flatten()(img_features)

    top = concatenate([osm_features, img_features])
    for i in range(0,number_of_repeats):
        top = Dense(256, activation='relu')(top)
        top = Dropout(0.5)(top)
    top = Dense(1, activation='sigmoid')(top)

    model = Model(inputs=[osm_features_input, img_features_input], outputs=top)
    return model

def build_full_mixed_model(osm_shape, img_shape = Input(shape=(299, 299, 3))):
    # Special case
    '''
    Tests with the mixed model without using features for cooking.
    :param osm_shape: shape of the osm data
    :param img_shape: shape of the imgs data
    :return:
    '''
    input_shape_osm = osm_shape

    number_of_repeats = 2

    input_tensor = img_shape
    from keras.applications.resnet50 import ResNet50
    from keras.utils import plot_model


    model_cnn = ResNet50(input_tensor=input_tensor, weights='imagenet', include_top=False)

    osm_features_input = Input(shape=input_shape_osm)
    osm_features = Dense(256, activation='relu')(osm_features_input)
    osm_features = Dropout(0.5)(osm_features)

    img_features = Flatten()(model_cnn.output)

    top = concatenate([osm_features, img_features])
    for i in range(0,number_of_repeats):
        top = Dense(256, activation='relu')(top)
        top = Dropout(0.5)(top)
    top = Dense(1, activation='sigmoid')(top)

    model = Model(inputs=[model_cnn.input, osm_features_input], outputs=top)
    model.summary()

    plot_model(model, to_file='TEST.png', show_shapes=True)

    return model

# Generate Whole Models
def get_top_models(models, datasets, Settings):
    '''
    Adds the right top models, now with proper knowledge of shapes of feature files.
    :param models: list of models where we will add new ones
    :param datasets: using information about databases
    :param Settings: and using information from Settings
    :return: models are generated and returned
    '''
    number_of_models = len(Settings["models"])
    print "## Adding ",number_of_models," top models."

    index = 0
    for model_settings in Settings["models"]:
        from ModelHandler.ModelTester import load_feature_file

        if model_settings["model_type"] is 'simple_cnn_with_top':
            model = models[index]

            if model_settings["evaluation_after_training"]:
                # special case, when we dont actually need any features or images - just evaluation
                if model_settings["pixels"] == 640:
                    input_shape = (2,2,2048)
                elif model_settings["pixels"] == 299:
                    input_shape = (1, 1, 2048)
                else:
                    print "uncoded model combination"
            else:
                filename_features_train = model_settings["filename_features_train"]
                train_data = load_feature_file(filename_features_train)
                input_shape = train_data.shape[1:]

            model[1] = build_img_only_top_model(input_shape=input_shape, number_of_repeats=model_settings["top_repeat_FC_block"])
            print model_settings["unique_id"], model

        elif model_settings["model_type"] is 'img_osm_mix':
            model = models[index]

            if model_settings["evaluation_after_training"]:
                # special case, when we dont actually need any features or images - just evaluation
                input_shape_osm = (594,)

                if model_settings["pixels"] == 640:
                    input_shape_img = (2,2,2048)
                elif model_settings["pixels"] == 299:
                    input_shape_img = (1, 1, 2048)
                else:
                    print "uncoded model combination"
            else:

                filename_features_train = model_settings["filename_features_train"]

                train_data = load_feature_file(filename_features_train)
                input_shape_img = train_data.shape[1:]

                dataset = datasets[ model_settings["dataset_pointer"] ]

                if not dataset.has_osm_loaded:
                    print "For this model type, we need OSM vectors, choose dataset accordingly."
                    Settings["interrupt"] = True
                    return None
                input_shape_osm = dataset.getShapeOfOsm()

                print "input_shape_osm", input_shape_osm

            if model_settings["special_case"] == 'base_cnn_custom_top':
                model[1] = build_img_osm_mix_model_custom_base_cnn_top(input_shape_img, input_shape_osm,
                                                   number_of_repeats=model_settings["top_repeat_FC_block"])
            else:
                model[1] = build_img_osm_mix_model(input_shape_img, input_shape_osm, number_of_repeats=model_settings["top_repeat_FC_block"])
            print model_settings["unique_id"], model

        elif model_settings["model_type"] is 'osm_only':
            model = models[index]

            if model_settings["evaluation_after_training"]:
                # special case, when we dont actually need any features or images - just evaluation
                input_shape = (594,)
            else:
                dataset = datasets[ model_settings["dataset_pointer"] ]

                if not dataset.has_osm_loaded:
                    print "For this model type, we need OSM vectors, choose dataset accordingly."
                    Settings["interrupt"] = True
                    return None

                if model_settings["special_case"] == 'OSM_Multiple_Radii':
                    dataset.expandOsmDataWithMultipleRadii(model_settings)

                input_shape = dataset.getShapeOfOsm()
                print "input_shape", input_shape

            model[0] = build_osm_only_model(input_shape=input_shape, number_of_repeats=model_settings["top_repeat_FC_block"], manual_width=model_settings["osm_manual_width"])
            print model_settings["unique_id"], model

            if model_settings["special_case"] == 'OSM_Multiple_Radii':
                print "Specially enhanced OSM model of shape:"
                model[0].summary()

        else:
            print "Yet to be programmed."

        index += 1
    return models

def report_models(models, Settings):
    '''
    Debug method - report all models
    :param models: list of models
    :param Settings: settings files to get the individual model settings
    :return:
    '''
    number_of_models = len(Settings["models"])
    print "## Adding ",number_of_models," top models."

    index = 0
    for model_settings in Settings["models"]:
        model = models[index]

        if model_settings["model_type"] is 'simple_cnn_with_top':
            filename_features_train = model_settings["filename_features_train"]


            print "^^^^^^ base part of IMG model"
            model[0].summary()
            print "^^^^^^ top part of IMG model"
            model[1].summary()

        elif model_settings["model_type"] is 'img_osm_mix':

            print "^^^^^^ base part of MIX model"
            model[0].summary()
            print "^^^^^^ top part of MIX model"
            model[1].summary()

        elif model_settings["model_type"] is 'osm_only':
            print "^^^^^^ main part of OSM model"
            model[0].summary()

        else:
            print "Yet to be programmed."

        index += 1

def get_cnn_models(Settings):
    '''
    Loads the base CNN part of models
    :param Settings: settings used to get individual model settings
    :return:
    '''
    models = []
    number_of_models = len(Settings["models"])
    print "## Loading",number_of_models,"models with their CNNs."

    for model_settings in Settings["models"]:

        if model_settings["model_type"] is 'simple_cnn_with_top' or model_settings["model_type"] is 'img_osm_mix':
            cnn_model = model_settings["cnn_model"]
            model_cnn = Models.get_model(cnn_model, pixels=model_settings["pixels"])
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

def split_model(model, start, end):
    '''
    Split model by the start and end flags - we get the subset of a model.
    # Thanks to https://github.com/fchollet/keras/issues/5074#issuecomment-274259404

    :param model: model to be split
    :param start: from layer
    :param end: to layer
    :return: subset of the model
    '''
    confs = model.get_config()
    weights = {l.name:l.get_weights() for l in model.layers}
    # split model
    kept_layers = set()
    for i, l in enumerate(confs['layers']):
        if i == 0:
            confs['layers'][0]['config']['batch_input_shape'] = model.layers[start].input_shape
        elif i < start or i > end:
            continue
        kept_layers.add(l['name'])
    # filter layers
    layers = [l for l in confs['layers'] if l['name'] in kept_layers]
    layers[1]['inbound_nodes'][0][0][0] = layers[0]['name']
    # set conf
    confs['layers'] = layers
    confs['input_layers'][0][0] = layers[0]['name']
    confs['output_layers'][0][0] = layers[-1]['name']

    print confs

    # create new model
    newModel = Model.from_config(confs)
    for l in newModel.layers:
        l.set_weights(weights[l.name])
    return newModel

# building models for fine tuning
def build_finetune_model(cnn, top, cut, input_shape):
    # Special case
    # experiments with finetuning whole models (base and top)
    from keras.models import Model

    for n in range(0,len(cnn.layers)):
        layer = cnn.layers[n]
        #print layer, type(layer), layer.get_config()
        #print layer.name, type(layer).__name__, layer, type(layer), layer.get_config()

        name = layer.get_config()['name']
        if 'add' in name:
            print n, layer

    print cut, cnn.layers[cut]

    cnn_rest_model = split_model(cnn, cut+1, len(cnn.layers))

    model_middle = Model(input=cnn_rest_model.input, output=top(cnn_rest_model.output))

    return model_middle

def join_two_models(one, two):
    '''
    Join two models in a chain after each other
    :param one: first model
    :param two: second model
    :return:  joined model
    '''
    from keras.models import Model
    finetune_model = Model(input=one.input, output=two(one.output))
    return finetune_model