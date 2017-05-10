import DatasetHandler.CreateDataset as CreateDataset
import ModelOI, ModelGenerator
from ModelHandler.ModelGenerator import build_top_model
from keras.utils import plot_model

from ModelHandler.ModelTester import TestTopModel
from Downloader.VisualizeHistory import visualize_histories, visualize_history
import ModelHandler.CreateModel.KerasApplicationsModels as Models

import datetime
# Manually writen experiments

def main(set, pixels, model_name='resnet50'):
    #TODO: Ideological skeleton
    '''
    # logically this should be:
    dataset = ModelOI.load_dataset(set, pixels, desired_size_of_images)
    cnn_models = ModelGenerator.get_cnn_models(model_names)
    cnn_model = ModelGenerator.get_cnn_model(model_name)
    top_models = ModelGenerator.get_top_models(...)
    top_model = ModelGenerator.get_top_model(...)

    ModelOI.cook_a_dataset(dataset) // ModelTester.prepare_cnn_model()

    visualization_filename = ModelOI.get_visualization_filename()
    ModelOI.save_visualization(cnn_model, top_model, visualization_filename)

    history = ModelTester.test_model(cnn_model, top_model, dataset) // [img_features, osm_features] = ModelOI.get_features(dataset)
    history_filename = ModelOI.get_history_filename()
    ModelOI.save_history(history, history_filename)
    '''

    local_folder = ModelOI.getLogDirectory()
    dataset = CreateDataset.load_custom(set, pixels, desired_number=5, seed=42)
    list_of_features = ModelOI.getFeaturesLists(dataset)

    histories = []
    histories_names = []
    specific_folder_name = 'size240imgs-pixelCountsVersus'

    for features in list_of_features:
        [model_name, filename_features_train, filename_features_test] = features

        now = datetime.datetime.now()
        specific_folder_name = str(now.day) + 'th' + '-' + str(now.hour) + '-' + str(now.minute) + '_' + model_name+"-"+str(pixels) # <day>th-hour-minute_experimentName
        target_folder = local_folder + specific_folder_name + '/'
        filename_history = target_folder + 'history_' + model_name + '.npy'
        img = local_folder + specific_folder_name+"-"+str(pixels)

        print filename_history
        history = TestTopModel(dataset, model_name, filename_features_train, filename_features_test, filename_history, img)
        histories.append(history)
        histories_names.append(model_name)

    img = local_folder + specific_folder_name + "_all_PX"+str(pixels)
    visualize_histories(histories, histories_names, show=False, save=True, save_path=img)

def test_generators(set, PIXELS):
    dataset = CreateDataset.load_custom(set, PIXELS, desired_number=10, seed=42)

    validation_split = 0.25
    [order, order_val, image_generator, size, image_generator_val, size_val] = dataset.getImageGenerator(validation_split, resize=None)
    #print order, order_val, image_generator, size, image_generator_val, size_val
    print image_generator, size, image_generator_val, size_val

    model_cnn = Models.resnet50()

    features = model_cnn.predict_generator(image_generator, steps=size, verbose=1)
    features_val = model_cnn.predict_generator(image_generator_val, steps=size_val, verbose=1)

    ### PATH NAMES
    local_folder = ModelOI.getLogDirectory()
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
