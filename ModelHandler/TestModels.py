import DatasetHandler.CreateDataset as CreateDataset

from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist
from ModelHandler.CreateModel.ModelsFunctions import load_features, build_top_model, train_top_model, save_model_history
from keras.utils import plot_model

from ModelHandler.CreateModel.ModelCooking import CookADataset
from ModelHandler.CreateModel.TopModel import TestTopModel
from Downloader.VisualizeHistory import visualize_histories, visualize_history
import ModelHandler.CreateModel.KerasApplicationsModels as Models

import datetime
# Manually writen experiments

def main(set, PIXELS):
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                    '/home/ekmek/Vitek/Logs/',
                    '/storage/brno2/home/previtus/Logs/',
                    ] #'/home/ekmek/Vitek/Logs-VALID ONE-run of 1200x set on 299x299 imgs/'
    local_folder = use_path_which_exists(log_folders)
    make_folder_ifItDoesntExist(local_folder+'shared/')

    dataset = CreateDataset.load_custom(set, PIXELS, desired_number=5, seed=42)

    list_of_features = CookADataset(dataset, local_folder=local_folder)
    histories = []
    histories_names = []
    specific_folder_name = 'size240imgs-pixelCountsVersus'

    for features in list_of_features:
        [model_name, filename_features_train, filename_features_test] = features

        now = datetime.datetime.now()
        specific_folder_name = str(now.day) + 'th' + '-' + str(now.hour) + '-' + str(now.minute) + '_' + model_name+"-"+str(PIXELS) # <day>th-hour-minute_experimentName
        target_folder = local_folder + specific_folder_name + '/'
        filename_history = target_folder + 'history_' + model_name + '.npy'
        img = local_folder + specific_folder_name+"-"+str(PIXELS)

        print filename_history
        history = TestTopModel(dataset, model_name, filename_features_train, filename_features_test, filename_history, img)
        histories.append(history)
        histories_names.append(model_name)

    img = local_folder + specific_folder_name + "_all_PX"+str(PIXELS)
    visualize_histories(histories, histories_names, show=False, save=True, save_path=img)

def test_generators(set, PIXELS):
    dataset = CreateDataset.load_custom(set, PIXELS, desired_number=None, seed=42)

    validation_split = 0.25
    [order, order_val, image_generator, size, image_generator_val, size_val] = dataset.getImageGenerator(validation_split, resize=None)
    #print order, order_val, image_generator, size, image_generator_val, size_val
    print image_generator, size, image_generator_val, size_val

    model_cnn = Models.resnet50()

    features = model_cnn.predict_generator(image_generator, steps=size, verbose=1)
    features_val = model_cnn.predict_generator(image_generator_val, steps=size_val, verbose=1)

    ### PATH NAMES
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                    '/home/ekmek/Vitek/Logs/',
                    '/storage/brno2/home/previtus/Logs/',
                    ] #'/home/ekmek/Vitek/Logs-VALID ONE-run of 1200x set on 299x299 imgs/'
    local_folder = use_path_which_exists(log_folders)
    make_folder_ifItDoesntExist(local_folder+'shared/')
    dataset_uid = dataset.unique_id+'GEN'
    model_name = 'resnet50'
    filename_features_train = local_folder + 'shared/' + 'features_train_' + dataset_uid + '_' + model_name + '.npy'
    filename_features_test = local_folder + 'shared/' + 'features_validation_' + dataset_uid + '_' + model_name + '.npy'
    print filename_features_train
    print filename_features_test
    ### END OF PATH NAMES

    import numpy as np
    np.save(open(filename_features_train, 'w'), features)
    np.save(open(filename_features_test, 'w'), features_val)
    features = np.load(open(filename_features_train))
    features_val = np.load(open(filename_features_test))

    #[feature_generator, feature_generator_val, size, size_val] = dataset.getFeatureGenerator(order, order_val,
    #                                                validation_split, features, features_val)
    #print feature_generator, feature_generator_val, size, size_val

    model = build_top_model(features.shape[1:], 3)
    #model.summary()
    #plot_model(model, to_file='tst.png', show_shapes=True)

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
    epochs = 50

    # HAS A PROBLEM # TRY JUST FIT AND NO GENERATOR
    [y, y_val] = dataset.getJustLabels(validation_split)
    history = model.fit(features, y,
              epochs=epochs, batch_size=32,
              validation_data=(features_val, y_val))

    #history = model.fit_generator(feature_generator, steps_per_epoch=size, epochs=epochs,
    #                              validation_data=feature_generator_val, validation_steps=size_val)

    history = history.history

    img = local_folder + "_graph_resnet50_via_gens_"+str(PIXELS)
    visualize_history(history, show=False, save=True, save_path=img)

    return 3

#name = '1200x_markable_299x299'
#pix = 299
#test_generators(name, pix)
