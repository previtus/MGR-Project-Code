# Runs tests on Models - will perform all calls to Keras functions like fit, predics, etc. and produce history of the
# process.
# Takes models as inputs.
# Can run either simple tests, or the more complicated ones separeted into:
# - train top > finetune CNN > finetune everything
# Can perform the more precise k-fold cross validation

from ModelHandler.ModelGenerator import build_top_model
from Downloader.ImageHelpers import len_
import numpy as np
from keras.utils import plot_model
from Downloader.VisualizeHistory import saveHistory, visualize_history

def cook_features(models, dataset, Settings):
    '''
    Makes sure that we have features available for the duo of model-dataset in our shared feature folder.
    If not, we will cook them.
    :param models: list of models (currently without their tops)
    :param dataset: dataset object
    :param Settings: settings
    :return:
    '''
    index = 0
    for model in models:
        model_settings = Settings["models"][index]
        from ModelHandler.ModelOI import get_feature_file_names, do_we_need_to_cook
        #ps: if this is in the header of the file, it causes mutual import of each other - and TF yells...

        [filename_features_train, filename_features_test] = get_feature_file_names(
            local_folder=Settings["folders"]["local_folder"], dataset_uid=dataset.unique_id, model_name=model_settings["cnn_model"])

        print [filename_features_train, filename_features_test]
        do_we_need_to_cook_bool = do_we_need_to_cook(filename_features_train, filename_features_test)

        if do_we_need_to_cook_bool:
            model_cnn = model[0]

            '''
            if x==None:
                [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)
                #[test_generator, val_generator, number_in_test, number_in_val] = dataset.getGenerators(validation_split=0.25)
            #predict_from_generators(test_generator, val_generator, number_in_test, number_in_val, filename_features_train, filename_features_test, model_cnn)
            predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model_cnn)
            '''

        index += 1
    return 1


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


# Test Whole model = Fit
def train_top_model(model, train_data, train_labels, epochs, validation_data, validation_labels, save_img_name=None):

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
    if save_img_name is not None:
        plot_model(model, to_file=save_img_name+'.png', show_shapes=True)

    history = model.fit(train_data, train_labels,
              epochs=epochs, batch_size=32,
              validation_data=(validation_data, validation_labels))

    #history = model.fit_generator(generator_train, steps_per_epoch, epochs=epochs,
    #                              validation_data=(generator_valid), validation_steps)

    return history.history

def TestTopModel(dataset, model_name, filename_features_train, filename_features_test, filename_history, img_name):
    [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)
    #[test_generator, val_generator, number_in_test, number_in_val] = dataset.getGenerators(validation_split=0.25)

    [train_data, train_labels, validation_data, validation_labels] = load_features(filename_features_train, filename_features_test, y, y_val)

    print "input shape of features", len_(train_data), "and labels", len_(train_labels)
    # Report feature output sizes

    # Try top models - regular with fixed size or the "heatmap"

    model = build_top_model(train_data.shape[1:], 3)

    epochs = 20 #150
    save_img_name = model_name
    history = train_top_model(model, train_data, train_labels, epochs, validation_data, validation_labels, save_img_name=None)

    save_model_history(history, filename_history, img_name)

    return history

def save_model_history(history, filename_history, filename_image):
    saveHistory(history, filename_history)
    visualize_history(history, show=False, save=True, save_path=filename_image)
