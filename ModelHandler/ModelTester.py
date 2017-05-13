# Runs tests on Models - will perform all calls to Keras functions like fit, predics, etc. and produce history of the
# process.
# Takes models as inputs.
# Can run either simple tests, or the more complicated ones separeted into:
# - train top > finetune CNN > finetune everything
# Can perform the more precise k-fold cross validation

from ModelHandler.ModelGenerator import build_simple_top_model
from Omnipresent import len_
import numpy as np
from keras.utils import plot_model
from Downloader.VisualizeHistory import saveHistory, visualize_history

def cook_features(models, datasets, Settings):
    '''
    Makes sure that we have features available for the duo of model-dataset in our shared feature folder.
    If not, we will cook them.
    :param models: list of models (currently without their tops)
    :param datasets: list of dataset object
    :param Settings: settings
    :return: number of ready models
    '''
    # cooking shared data
    [x, y, x_val, y_val] = [None, None, None, None]

    index = 0
    for model in models:
        model_settings = Settings["models"][index]

        # TODO: MODEL_TYPE_SPLIT

        if model_settings["model_type"] is 'simple_cnn_with_top':

            dataset = datasets[ model_settings["dataset_pointer"] ]
            from ModelHandler.ModelOI import get_feature_file_names, do_we_need_to_cook
            #ps: if this is in the header of the file, it causes mutual import of each other - and TF yells...

            filename_features_train = model_settings["filename_features_train"]
            filename_features_test = model_settings["filename_features_test"]
            do_we_need_to_cook_bool = do_we_need_to_cook(filename_features_train, filename_features_test)
            print "Looking up files:", filename_features_train, filename_features_test

            if do_we_need_to_cook_bool:
                model_cnn = model[0]
                cooking_method = model_settings["cooking_method"]

                print "We need to cook, chosen method is", cooking_method
                #if True:
                if cooking_method == 'direct':
                    if x is None:
                        [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=model_settings["validation_split"])
                        print len_(x)

                    predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model_cnn)

                #if True:
                elif cooking_method == 'generators':
                    [order, order_val, image_generator, size, image_generator_val, size_val] = dataset.getImageGenerator(validation_split=model_settings["validation_split"])
                    print len_(order)

                    predict_from_generators(image_generator, image_generator_val, size, size_val, filename_features_train, filename_features_test, model_cnn)

            else:
                print "No need to cook, the files already exist"
        elif model_settings["model_type"] is 'osm_only':
            # No need to cook features from images in this case
            print "Chosen model type (", model_settings["model_type"] ,") doesn't require features to be cooked and loaded."
        index += 1
    return index

def test_models(models, datasets, Settings):
    '''
    Runs test on all model - dataset pairs from models.
    :param models: array of models to run
    :param dataset:
    :param Settings:
    :return:
    '''
    number_of_models = len(Settings["models"])
    print "## Testing",number_of_models,"models."

    histories = []
    index = 0
    for model in models:
        model_settings = Settings["models"][index]
        dataset = datasets[ model_settings["dataset_pointer"] ]

        print "Testing", model_settings["unique_id"], model
        history = test_model(model, dataset, model_settings)
        histories.append(history)

        index += 1
    return histories

def test_model(model, dataset, model_settings):
    history = None
    # TODO: MODEL_TYPE_SPLIT

    if model_settings["model_type"] is 'simple_cnn_with_top':

        filename_features_train = model_settings["filename_features_train"]
        filename_features_test = model_settings["filename_features_test"]

        [y, y_val] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])
        [train_data, train_labels, validation_data, validation_labels] = load_features(filename_features_train, filename_features_test, y, y_val)

        print "input shape of features", len_(train_data), "and labels", len_(train_labels)

        top_model = model[1]
        history = train_top_model(top_model, model_settings, train_data, train_labels, validation_data, validation_labels)
    elif model_settings["model_type"] is 'osm_only':

        [osm, osm_val] = dataset.getDataLabels_split_only_osm(validation_split=model_settings["validation_split"])
        [y, y_val] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])

        osm_model = model[0]
        history = train_top_model(osm_model, model_settings, osm, y, osm_val, y_val)

    else:
        print "Yet to be programmed."

    return history

# Generate Feature files = Predict
def predict_from_generators(test_generator, val_generator, number_in_test, number_in_val, filename_features_train, filename_features_test, model):
    # generators should yield:
    bottleneck_features_train = model.predict_generator(test_generator, steps=number_in_test,verbose=1)
    np.save(open(filename_features_train, 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict_generator(val_generator, steps=number_in_val,verbose=1)
    np.save(open(filename_features_test, 'w'), bottleneck_features_validation)

def predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model):
    # dimensions of x are (num,3,x_dim, y_dim) = (75, 3, 150, 150)
    bottleneck_features_train = model.predict(x,verbose=1)
    np.save(open(filename_features_train, 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict(x_val,verbose=1)
    np.save(open(filename_features_test, 'w'), bottleneck_features_validation)

def load_features(filename_features_train, filename_features_test, y, y_val):
    train_data = np.load(open(filename_features_train))
    train_labels = np.array(y)

    validation_data = np.load(open(filename_features_test))
    validation_labels = np.array(y_val)
    return [train_data, train_labels, validation_data, validation_labels]

def load_feature_file(path):
    '''
    Just loads the features stored in one file.
    :param path:
    :return:
    '''
    try:
        data = np.load(open(path))
        return data
    except:
        print "Failed to load file", path
        return 0

# Test Whole model = Fit
def train_top_model(model, model_settings, train_data, train_labels, validation_data, validation_labels):

    model.compile(optimizer=model_settings["optimizer"], loss=model_settings["loss_func"], metrics=model_settings["metrics"])

    history = model.fit(train_data, train_labels,
              epochs=model_settings["epochs"], batch_size=32,
              validation_data=(validation_data, validation_labels))

    #history = model.fit_generator(generator_train, steps_per_epoch, epochs=epochs,
    #                              validation_data=(generator_valid), validation_steps)

    return history.history
