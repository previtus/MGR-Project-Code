# Handles data input and output for Models
# For example:
# - loading data like img_features, osm_features, scores
# - provide final Model saving and loading

from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist
import os
import ModelHandler.CreateModel.KerasApplicationsModels as Models
import DatasetHandler.CreateDataset

def prepare_folders(Settings, dataset):
    '''
    Figures folder paths which will be used in experiment (local folder with history file, graphs, model file and also
    the shared folder where features are saved. Also the paths for filename_features_train, filename_features_test for
    for each model. Saves these paths into Settings.
    :param Settings: This is a travelling dictionary with all the settings, we will add folder settings there
    :return:
    '''
    folders = {}
    folders["local_folder"] = getLogDirectory()
    folders["features_folder"] = folders["local_folder"] + 'shared/'
    folders["together_graph_file"] = folders["local_folder"] + Settings["experiment_name"] + '-' + Settings["dataset_name"] + '.png'
    folders["together_graph_title"] = Settings["experiment_name"] + '-' + Settings["dataset_name"]

    Settings["folders"] = folders

    for model_settings in Settings["models"]:
        are_we_using_generators = (model_settings["cooking_method"] == 'generators')

        [filename_features_train, filename_features_test] = get_feature_file_names(
            local_folder=Settings["folders"]["local_folder"], dataset_uid=dataset.unique_id, model_name=model_settings["cnn_model"],
            are_we_using_generators=are_we_using_generators)

        model_settings["filename_features_train"] = filename_features_train
        model_settings["filename_features_test"] = filename_features_test
        # TODO: have its own nice path
        model_settings["model_image_name"] = filename_features_test + '.png'
        history_file = folders["local_folder"] + 'history_' + model_settings["cnn_model"] + model_settings["unique_id"] + '.npy'
        model_settings["history_file"] = history_file
        model_settings["history_graph"] = history_file + '.png'

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

# Outputs

def save_visualizations(models, Settings):
    '''
    Save visualizations of the models, if we have set it in Settings
    :param models:
    :param Settings:
    :return:
    '''
    index = 0
    for model in models:
        model_settings = Settings["models"][index]
        if model_settings["save_visualization"]:
            from keras.utils import plot_model
            #cnn_model = model[0]
            #plot_model(cnn_model, to_file=model_settings["model_image_name"]+'_cnn.png', show_shapes=True)
            top_model = model[1]
            plot_model(top_model, to_file=model_settings["model_image_name"], show_shapes=True)

        index += 1

def save_histories(histories, Settings):
    '''
    Save histories into .npy files, which can be used to reproduce the results.
    :param histories:
    :param Settings:
    :return:
    '''
    index = 0

    for history in histories:
        model_settings = Settings["models"][index]
        from Downloader.VisualizeHistory import saveHistory
        saveHistory(history, model_settings["history_file"])
        index += 1

        print "history saved >>", model_settings["history_file"]

def graph_histories(histories, Settings):
    '''
    Graphs histories according to Settings["graph_histories"] ~ ['all',[]] #['all',[],[0,2]]
    :param histories:
    :param Settings:
    :return:
    '''

    for setting in Settings["graph_histories"]:
        from Downloader.VisualizeHistory import visualize_history, visualize_histories

        if setting == 'all':
            # graph each of them into their own image
            print 'all'

            index = 0
            for history in histories:
                model_settings = Settings["models"][index]
                graph_file = model_settings["history_graph"]

                custom_title = 'One:' + model_settings["unique_id"]
                visualize_history(history, show=False, save=True, save_path=graph_file, custom_title=custom_title)
                index +=1

                print "graph saved >>", graph_file

        elif setting == 'together':
            # graph all of them into one image
            print 'together'

            names = []
            index = 0
            for history in histories:
                custom_name = Settings["models"][index]["unique_id"]
                names.append(custom_name)
                index +=1

            graph_file = Settings["folders"]["together_graph_file"]
            custom_title = 'All:' + Settings["folders"]["together_graph_title"]
            visualize_histories(histories, names, plotvalues='loss', show=False, save=True, save_path=graph_file, custom_title=custom_title)

            print "graph saved >>", graph_file

        elif setting == []:
            continue
        else:
            # graph combination ~ [0,1]
            print 'combination'
            histories_subset = []
            subset_names = []
            combination_txt = ' '
            for i in setting:
                if i >= 0 and i < len(histories):
                    histories_subset.append(histories[i])
                    custom_name = Settings["models"][i]["unique_id"]
                    subset_names.append(custom_name)
                    combination_txt += str(i)+' '

            graph_file = Settings["folders"]["together_graph_file"] + 'Combination [' + combination_txt + '] ' + '.png'
            custom_title = 'Combination [' + combination_txt + ']: ' + Settings["folders"]["together_graph_title"]
            visualize_histories(histories_subset, subset_names, plotvalues='loss', show=False, save=True, save_path=graph_file, custom_title=custom_title)
            print "graph saved >>", graph_file

    return 0

##############################################

def getFeaturesLists(dataset):
    # TODO: DEL

    local_folder = getLogDirectory()
    #with_models = Models.all_model_names()
    with_models = ['resnet50']
    list_of_features = CookADataset(dataset, with_models, local_folder=local_folder)

    return list_of_features

def CookADataset(dataset, with_models, local_folder):
    # TODO: DEL
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
