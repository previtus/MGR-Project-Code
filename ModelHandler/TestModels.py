import DatasetHandler.CreateDataset as CreateDataset

from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist
from ModelHandler.CreateModel.ModelsFunctions import load_features, build_top_model, train_top_model, save_model_history

from ModelHandler.CreateModel.ModelCooking import CookADataset
from ModelHandler.CreateModel.TopModel import TestTopModel
from Downloader.VisualizeHistory import visualize_histories, visualize_history
import ModelHandler.CreateModel.KerasApplicationsModels as Models

import datetime
# Test functions to handle models

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
    dataset = CreateDataset.load_custom(set, PIXELS, desired_number=5, seed=42)

    validation_split = 0.25
    [order, image_generator, size] = dataset.getImageGenerator(validation_split, resize=None)
    print order, image_generator, size

    model_cnn = Models.resnet50()

    features_train = model_cnn.predict_generator(image_generator, steps=size,verbose=1)
    print features_train

    all_features = features_train
    [order, feature_generator] = dataset.getFeatureGenerator(order, validation_split, all_features, resize=None)
    print features_train.shape[1:]

    model = build_top_model(features_train.shape[1:], 3)
    model.summary()

    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])

    epochs = 50
    # history = model.fit_generator(feature_generator, steps_per_epoch=size, epochs=epochs) # HAS A PROBLEM

    # visualize_history(history)

    return 3

name = '1200x_markable_299x299'
pix = 299
test_generators(name, pix)
