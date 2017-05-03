import ModelHandler.CreateModel.KerasApplicationsModels as Models

from ModelHandler.CreateModel.functions_for_vgg16 import doWeNeedToCook, predict_and_save_features, load_features, build_top_model

def CookADataset(dataset, local_folder):
    '''
    Will cook all feature files for a dataset
    :param dataset: dataset object
    :param local_folder:
    :return:
    '''
    # Load dataset, report input sizes
    print "### Cooking for dataset"
    print "w*h*ch:", dataset.img_width, "x", dataset.img_height, "x 3"
    dataset_uid = dataset.unique_id
    [x, y, x_val, y_val] = [None, None, None, None]
    list_of_feature_files = []

    import random
    random.seed(None)

    # Cook features for various models
    #all_models = Models.all_model_names()
    all_models = ['resnet50']

    for model_name in all_models:
        #print model_name

        filename_features_train = local_folder+'shared/'+'features_train_'+dataset_uid+'_'+model_name+'.npy'
        filename_features_test = local_folder+'shared/'+'features_validation_'+dataset_uid+'_'+model_name+'.npy'

        if doWeNeedToCook(filename_features_train, filename_features_test):
            if x==None:
                [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)

            model_cnn = Models.get_model(model_name)
            predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model_cnn)

        list_of_feature_files.append([model_name, filename_features_train, filename_features_test])

    return list_of_feature_files
