# Handles data input and output for Models
# For example:
# - loading data like img_features, osm_features, scores
# - provide final Model saving and loading

from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist
import os
import ModelHandler.CreateModel.KerasApplicationsModels as Models
import DatasetHandler.CreateDataset
from Omnipresent import save_job_report_page, send_mail
import Downloader.VisualizeHistory

def prepare_folders(Settings, datasets, verbose=False):
    '''
    Figures folder paths which will be used in experiment (local folder with history file, graphs, model file and also
    the shared folder where features are saved. Also the paths for filename_features_train, filename_features_test for
    for each model. Saves these paths into Settings.
    :param Settings: This is a travelling dictionary with all the settings, we will add folder settings there
    :return:
    '''

    folders = {}
    # Local folder
    log_folder = getLogDirectory()
    experiment_name = Settings["experiment_name"]
    # make /<experiment>/ history and model_shapes folder structure
    make_folder_ifItDoesntExist(log_folder+experiment_name+'/')
    folders["local_logs_folder"] = log_folder + experiment_name+'/'

    # VERSION A - folders history and models
    folders["history_folder"] = folders["local_logs_folder"]+'history/'
    folders["models_folder"] = folders["local_logs_folder"]+'models/'
    make_folder_ifItDoesntExist(folders["history_folder"])
    make_folder_ifItDoesntExist(folders["models_folder"])

    # VERSION B - just with names history_* and models_*
    '''
    folders["history_folder"] = folders["local_logs_folder"]+'history_'
    folders["models_folder"] = folders["local_logs_folder"]+'models_'
    '''

    folders["shared_features_folder"] = getSharedDirectory()

    folders["together_graph_filename"] = folders["local_logs_folder"] + "graph_together_" + experiment_name + '.png'
    folders["together_graph_title"] = experiment_name + " together graph"

    folders["report_txt_file"] = folders["local_logs_folder"] + "report.txt"
    folders["report_html_file"] = folders["local_logs_folder"] + "report_"

    Settings["folders"] = folders

    for model_settings in Settings["models"]:
        dataset = datasets[ model_settings["dataset_pointer"] ]
        [filename_features_train, filename_features_test] = get_feature_file_names(
            shared_folder=Settings["folders"]["shared_features_folder"], dataset_uid=dataset.unique_id, model_name=model_settings["cnn_model"])

        model_settings["filename_features_train"] = filename_features_train
        model_settings["filename_features_test"] = filename_features_test

        model_identificator = model_settings["dataset_name"]+"_"+model_settings["unique_id"]+"_"+str(model_settings["epochs"])
        model_settings["history_filename"] = Settings["folders"]["history_folder"] + model_identificator+".npy"
        model_settings["graph_filename"] = Settings["folders"]["local_logs_folder"] + "graph_" + model_identificator+".png"

        model_identificator_for_shape = model_settings["unique_id"]+"_"+model_settings["cnn_model"]
        model_settings["model_shape_filename"] = Settings["folders"]["models_folder"] + model_identificator_for_shape+".png"
        model_settings["model_filename"] = Settings["folders"]["models_folder"] + model_identificator_for_shape+".h5"

        model_settings["model_save"] = 1 # 0 = don't save, 1 = save only top, 2 = save it all

    if verbose:
        print "Folder paths dump:"
        print Settings["folders"]["shared_features_folder"]
        print Settings["folders"]["local_logs_folder"]
        print Settings["folders"]["report_txt_file"]

        print Settings["folders"]["together_graph_filename"]
        for model_settings in Settings["models"]:
            print model_settings["graph_filename"]
        for model_settings in Settings["models"]:
            print model_settings["history_filename"]
        for model_settings in Settings["models"]:
            print model_settings["model_shape_filename"]
        for model_settings in Settings["models"]:
            print model_settings["model_filename"]
        for model_settings in Settings["models"]:
            print model_settings["filename_features_train"]
        for model_settings in Settings["models"]:
            print model_settings["filename_features_test"]

    return Settings

def getLogDirectory():
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                    '/home/ekmek/Vitek/Logs/',
                    '/storage/brno2/home/previtus/Logs/'
                    ] #'/home/ekmek/Vitek/Logs-VALID ONE-run of 1200x set on 299x299 imgs/'
    local_folder = use_path_which_exists(log_folders)
    make_folder_ifItDoesntExist(local_folder+'shared/')

    return local_folder

def getSharedDirectory():
    shared_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                    '/home/ekmek/Vitek/Logs/',
                    '/storage/brno2/home/previtus/Logs/'
                    ]
    shared_folder = use_path_which_exists(shared_folders)
    make_folder_ifItDoesntExist(shared_folder+'shared/')
    shared_folder += 'shared/'
    return shared_folder

def load_dataset(Settings):
    '''
    Loads datasets according to the Settings parameters "dataset_name", "pixels", "number_of_images", "seed"
    :param Settings:
    :return:
    '''
    datasets = []
    index = 0

    num = 0
    for model_setting in Settings["models"]:
        if model_setting["dataset_pointer"] == -1:
            num+=1
    print "## Loading", num, " unique datasets:"
    debug_ptrs = []

    for model_setting in Settings["models"]:
        ptr = model_setting["dataset_pointer"]
        if ptr == -1:
            dataset = DatasetHandler.CreateDataset.load_custom(model_setting["dataset_name"], model_setting["pixels"],
                    desired_number=model_setting["number_of_images"], seed=model_setting["seed"])
            datasets.append(dataset)
            model_setting["dataset_pointer"] = index

            debug_ptrs.append(index)
            index += 1

    print "Datasets:", debug_ptrs, datasets

    return datasets

# Cooking
def do_we_need_to_cook(filename_features_train, filename_features_test):
    return not(os.path.exists(filename_features_train) and os.path.getsize(filename_features_train) > 0
        and os.path.exists(filename_features_test) and os.path.getsize(filename_features_test) > 0)

def get_feature_file_names(shared_folder, dataset_uid, model_name):
    '''
    :param shared_folder: taken from getSharedDirectory()
    :param dataset_uid: taken from dataset.unique_id
    :param model_name: can be 'resnet50'
    :return:
    '''

    filename_features_train = shared_folder+'features_train_'+dataset_uid+'_'+model_name+'.npy'
    filename_features_test = shared_folder+'features_validation_'+dataset_uid+'_'+model_name+'.npy'
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
            plot_model(top_model, to_file=model_settings["model_shape_filename"], show_shapes=True)

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
        saveHistory(history, model_settings["history_filename"])
        index += 1

        print "history saved >>", model_settings["history_filename"]

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
                graph_file = model_settings["graph_filename"]

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

            graph_file = Settings["folders"]["together_graph_filename"]
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

            graph_file = Settings["folders"]["together_graph_filename"] + 'Combination [' + combination_txt + '] ' + '.png'
            custom_title = 'Combination [' + combination_txt + ']: ' + Settings["folders"]["together_graph_title"]
            visualize_histories(histories_subset, subset_names, plotvalues='loss', show=False, save=True, save_path=graph_file, custom_title=custom_title)
            print "graph saved >>", graph_file

    return 0

def generate_report_string(Settings):
    text = ''
    text += ("Experiment [%s] report: \n" % (Settings["experiment_name"]))
    text += ("With %s models: \n" % (len(Settings["models"])))
    for model_settings in Settings["models"]:
        text += ("%s \n" % (model_settings["unique_id"]))
        text += ("Trained for %s epochs with %s optimizer \n" % (model_settings["epochs"], model_settings["optimizer"]))
        text += ("Used dataset: %s with %s images \n" % (model_settings["dataset_name"], model_settings["number_of_images"]))
        text += ("\n")
    return text

def save_report(Settings):
    '''
    Saves report of the most important settings.
    :param models:
    :param Settings:
    :return:
    '''
    with open(Settings["folders"]["report_txt_file"], "w") as text_file:
        text_file.write(generate_report_string(Settings))

    print "report saved >>", Settings["folders"]["report_txt_file"]


def save_models(models, Settings):
    '''
    Saves the trained models alongside with the experiments settings.
    :param models:
    :param Settings:
    :return:
    '''

    index = 0
    for model in models:
        model_settings = Settings["models"][index]

        if model_settings["model_type"] is 'simple_cnn_with_top':
            if model_settings["model_save"] > 0:
                model[1].save(model_settings["model_filename"]+'_top.h5')  # creates a HDF5 file
                print "model saved >>", model_settings["model_filename"]+'_top.h5'
            if model_settings["model_save"] > 1:
                model[0].save(model_settings["model_filename"]+'_cnn.h5')  # creates a HDF5 file
                print "model saved >>", model_settings["model_filename"]+'_cnn.h5'

        else:
            print "Yet to be programmed."

        index += 1

def load_model(path):
    from keras.models import load_model
    return load_model(path)


# Further potentially useful reports

def send_mail_with_graph(Settings):
    subject='Report of Experiment finishing'
    message=generate_report_string(Settings)
    attachment_path=None

    if 'together' in Settings["graph_histories"]:
        attachment_path = Settings["folders"]["together_graph_filename"]

    print "## Sending report mail with attachment ", attachment_path
    send_mail(subject, message, attachment_path)

def save_metacentrum_report(Settings):
    job_id = Settings["job_id"]
    if job_id <> '':
        print "## Downloading ", job_id+'.html'
        save_job_report_page(Settings["folders"]["report_html_file"], job_id)
    else:
        print "## Downloading of job page failed, we don't know job_id", job_id
