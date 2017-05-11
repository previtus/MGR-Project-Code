# Handles data input and output for Models
# For example:
# - loading data like img_features, osm_features, scores
# - provide final Model saving and loading

from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist
import os
import ModelHandler.CreateModel.KerasApplicationsModels as Models
import DatasetHandler.CreateDataset

def prepare_folders(Settings):
    '''
    Figures folder paths which will be used in experiment (local folder with history file, graphs, model file and also
    the shared folder where features are saved.
    Saves these paths into Settings.
    :param Settings: This is a travelling dictionary with all the settings, we will add folder settings there
    :return:
    '''
    folders = {}
    folders["local_folder"] = getLogDirectory()
    folders["features_folder"] = folders["local_folder"] + 'shared/'

    Settings["folders"] = folders
    return Settings

def getLogDirectory():
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                    '/home/ekmek/Vitek/Logs/',
                    '/storage/brno2/home/previtus/Logs/',
                    ] #'/home/ekmek/Vitek/Logs-VALID ONE-run of 1200x set on 299x299 imgs/'
    local_folder = use_path_which_exists(log_folders)
    make_folder_ifItDoesntExist(local_folder+'shared/')

    return local_folder

def load_dataset(Settings):
    '''
    Loads dataset according to the Settings parameters "dataset_name", "pixels", "number_of_images", "seed"
    :param Settings:
    :return:
    '''
    dataset = DatasetHandler.CreateDataset.load_custom(Settings["dataset_name"], Settings["pixels"],
                    desired_number=Settings["number_of_images"], seed=Settings["seed"])
    return dataset

##############################################
def getFeaturesLists(dataset):
    local_folder = getLogDirectory()
    #with_models = Models.all_model_names()
    with_models = ['resnet50']
    list_of_features = CookADataset(dataset, with_models, local_folder=local_folder)

    return list_of_features

# Cooking
def do_we_need_to_cook(filename_features_train, filename_features_test):
    return not(os.path.exists(filename_features_train) and os.path.getsize(filename_features_train) > 0
        and os.path.exists(filename_features_test) and os.path.getsize(filename_features_test) > 0)

def get_feature_file_names(local_folder, dataset_uid, model_name, are_we_using_generators=False):
    '''
    :param local_folder: taken from getLogDirectory()
    :param dataset_uid: taken from dataset.unique_id
    :param model_name: can be 'resnet50'
    :return:
    '''
    add = ''
    if are_we_using_generators:
        add = '_GEN'

    filename_features_train = local_folder+'shared/'+'features_train_'+dataset_uid+'_'+model_name+add+'.npy'
    filename_features_test = local_folder+'shared/'+'features_validation_'+dataset_uid+'_'+model_name+add+'.npy'
    return [filename_features_train, filename_features_test]


def CookADataset(dataset, with_models, local_folder):
    '''
    Will cook all feature files for a dataset
    :param dataset: dataset object
    :param local_folder:
    :return: list of [model_name, filename_features_train, filename_features_test]
    '''
    # Load dataset, report input sizes
    print "### Cooking for dataset"
    print "w*h*ch:", dataset.img_width, "x", dataset.img_height, "x 3"
    dataset_uid = dataset.unique_id
    [x, y, x_val, y_val] = [None, None, None, None]
    list_of_feature_files = []

    import random
    random.seed(None)

    for model_name in with_models:
        #print model_name
        [filename_features_train, filename_features_test] = get_feature_file_names(local_folder, dataset_uid, model_name)

        if do_we_need_to_cook(filename_features_train, filename_features_test):
            if x==None:
                [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)
                #[test_generator, val_generator, number_in_test, number_in_val] = dataset.getGenerators(validation_split=0.25)

            model_cnn = Models.get_model(model_name)

            #predict_from_generators(test_generator, val_generator, number_in_test, number_in_val, filename_features_train, filename_features_test, model_cnn)

            #import ModelHandler.ModelTester
            #ModelHandler.ModelTester.predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model_cnn)

        list_of_feature_files.append([model_name, filename_features_train, filename_features_test])

    return list_of_feature_files
