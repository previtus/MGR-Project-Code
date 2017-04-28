import ModelHandler.CreateModel.KerasApplicationsModels as Models

from ModelHandler.CreateModel.functions_for_vgg16 import doWeNeedToCook, predict_and_save_features, load_features, build_top_model


def CookADataset(dataset, local_folder, name_of_the_experiment):
    '''
    Will cook all feature files for a dataset
    :param dataset: dataset object
    :param local_folder:
    :param name_of_the_experiment:
    :return:
    '''
    # Load dataset, report input sizes
    print "### Cooking for dataset"
    print "w*h*ch:", dataset.img_width, "x", dataset.img_height, "x 3"
    [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)
    dataset_uid = dataset.unique_id

    list_of_feature_files = []

    import random
    random.seed(None)

    # Cook features for various models
    all_models = Models.all_models()

    for model_ in all_models:
        model_name = model_[0]
        model_cnn = model_[1]
        print model_name, model_cnn

        filename_features_train = local_folder+'shared/'+'features_train_'+dataset_uid+'_'+model_name+'.npy'
        filename_features_test = local_folder+'shared/'+'features_validation_'+dataset_uid+'_'+model_name+'.npy'


        if doWeNeedToCook(filename_features_train, filename_features_test):
            predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model_cnn)
        [train_data, train_labels, validation_data, validation_labels] = load_features(filename_features_train, filename_features_test, y, y_val)

        list_of_feature_files.append([model_name, filename_features_train, filename_features_test])

    # Report feature output sizes

    # Try top models - regular with fixed size or the "heatmap"
    #    model = build_top_model(train_data.shape[1:], 3)
    #    model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['mean_absolute_error'])
    #    plot_model(model, to_file='TEST.png', show_shapes=True)

    return list_of_feature_files
