# Handles data input and output for Models
# For example:
# - loading data like img_features, osm_features, scores
# - provide final Model saving and loading

from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist
import os
import DatasetHandler.CreateDataset
from DatasetHandler.DataAugmentation import handle_noncanon_dataset
from Omnipresent import save_job_report_page, send_mail, len_

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
    job_str = ''
    if Settings["job_id"] <> '':
        job_str = Settings["job_id"] + '_'

    make_folder_ifItDoesntExist(log_folder+job_str+experiment_name+'/')
    folders["local_logs_folder"] = log_folder + job_str + experiment_name+'/'

    # folders history and models
    folders["history_folder"] = folders["local_logs_folder"]+'history/'
    folders["models_folder"] = folders["local_logs_folder"]+'models/'
    make_folder_ifItDoesntExist(folders["history_folder"])
    make_folder_ifItDoesntExist(folders["models_folder"])
    folders["shared_features_folder"] = getSharedDirectory()
    folders["together_graph_filename"] = folders["local_logs_folder"] + "graph_together_" + experiment_name + '.png'
    folders["together_graph_title"] = experiment_name + " together graph"
    folders["report_txt_file"] = folders["local_logs_folder"] + "report.txt"
    folders["report_html_file"] = folders["local_logs_folder"] + "report_"

    Settings["folders"] = folders

    # individual model settings, manage their feature paths
    for model_settings in Settings["models"]:
        dataset = datasets[ model_settings["dataset_pointer"] ]

        cnn_model = model_settings["cnn_model"]
        if model_settings["special_case"] == 'base_cnn_custom_top':
            cnn_model += "_SPECIAL-CUSTOM-TOP" + model_settings["mark"]

        [filename_features_train, filename_features_test] = get_feature_file_names(
            shared_folder=Settings["folders"]["shared_features_folder"], dataset_uid=dataset.unique_id, model_name=cnn_model)

        model_settings["filename_features_train"] = filename_features_train
        model_settings["filename_features_test"] = filename_features_test

        # Finetune feature filenames
        if model_settings["finetune"]:
            number_of_layers_unlocked = model_settings["finetune_num_of_cnn_layers"]

            [finetune_features_train, finetune_features_test] = get_feature_file_names(
            shared_folder=Settings["folders"]["shared_features_folder"], dataset_uid=dataset.unique_id, model_name=model_settings["cnn_model"],
            cut=number_of_layers_unlocked)

            model_settings["finetune_features_train"] = finetune_features_train
            model_settings["finetune_features_test"] = finetune_features_test

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

        for model_settings in Settings["models"]:
            if model_settings["finetune"]:
                print model_settings["finetune_features_train"]
        for model_settings in Settings["models"]:
            if model_settings["finetune"]:
                print model_settings["finetune_features_test"]

    return Settings

def getLogDirectory():
    '''
    Get established Log directories. Code will use the one of these paths which is available on the machine.
    :return: working path to Logs directory
    '''
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                    '/home/ekmek/Vitek/Logs/',
                    '/storage/plzen1/home/previtus/Logs/'
                    ]
    local_folder = use_path_which_exists(log_folders)
    make_folder_ifItDoesntExist(local_folder+'shared/')

    return local_folder

def getSharedDirectory():
    '''
    Get established Log directories. Code will use the one of these paths which is available on the machine.
    :return: working path to Logs/shared directory
    '''
    shared_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                    '/home/ekmek/Vitek/Logs/',
                    '/storage/plzen1/home/previtus/Logs/'
                    ]
    shared_folder = use_path_which_exists(shared_folders)
    make_folder_ifItDoesntExist(shared_folder+'shared/')
    shared_folder += 'shared/'
    return shared_folder

def load_dataset(Settings):
    '''
    Loads datasets according to the Settings parameters "dataset_name", "pixels", "number_of_images", "seed".
    Also manages shuffling and other initial editations of the dataset.
    :param Settings:
    :return: dataset object
    '''
    datasets = []
    index = 0

    num = 0
    for model_settings in Settings["models"]:
        if model_settings["dataset_pointer"] == -1:
            num+=1
    print "## Loading", num, " unique datasets:"
    debug_ptrs = []

    for model_settings in Settings["models"]:

        ptr = model_settings["dataset_pointer"]
        if ptr == -1:
            if model_settings["noncanon_dataset"] <> '':
                handle_noncanon_dataset(Settings, model_settings)
                model_settings["dump_file_override"] = model_settings["dump_file_expanded"]

            dataset = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                    desired_number=model_settings["number_of_images"], seed=model_settings["seed"], filename_override=model_settings["dump_file_override"])

            if model_settings["special_case"] == 'debug':
                dataset.debug_print_first(200)

            # Shuffling
            #  shuffle the individual block of images from different places, to get more uniformly distributed data
            #  but be careful not to separate [img1,osm1,vec1] and [img2,osm1,osm1] into training and valid sets
            #  which in osm_only model would both result in same data: [_,osm1,vec1]
            #  This would also be problematic in mixed model case.
            # ps: different shuffle should end up with different dataset.unique_id, as the feature files are also different.
            if model_settings["shuffle_dataset"]:
                if model_settings["shuffle_dataset_method"] == 'default-same-segment':
                    dataset.randomize_all_list_order_deterministically_same_segment(model_settings["seed"])

            else:
                dataset.unique_id = dataset.unique_id + "_notshuffled"

            # OSM data projection
            #  We can try edit the osm vectors to have nicer characteristics for CNNs
            # ps: no need to mark this down into dataset.unique_id as this doesn't touch images
            if model_settings["edit_osm_vec"] == 'booleans':
                dataset.cast_osm_to_bool()

            elif model_settings["edit_osm_vec"] == 'low-mid-high':
                dataset.cast_osm_to_one_hot_categories()

            elif model_settings["edit_osm_vec"] == 'log':
                dataset.log_the_osm()

            if model_settings["osm_only_unique_osms"] and model_settings["model_type"] == 'osm_only':
                # yup allow thin only for osm only model - that's when we have dualities
                dataset.remove_dual_osms()

            if model_settings["test_existence_of_images"]:
                dataset.test_existence_of_all_images()

            if model_settings["special_case"] == 'debug':
                print "DEBUG OUTPUT ABOUT"
                print dataset
                print dataset.plotHistogram(save_to_pdf=True)

            datasets.append(dataset)
            model_settings["dataset_pointer"] = index

            debug_ptrs.append(index)
            index += 1

    print "Datasets:", debug_ptrs, datasets

    return datasets

# Cooking
def do_we_need_to_cook(filename_features_train, filename_features_test):
    '''
    Checks for the existence of cooked feature files.
    :param filename_features_train: path to training features
    :param filename_features_test: path to testing features
    :return:
    '''
    return not(os.path.exists(filename_features_train) and os.path.getsize(filename_features_train) > 0
        and os.path.exists(filename_features_test) and os.path.getsize(filename_features_test) > 0)

def get_feature_file_names(shared_folder, dataset_uid, model_name, cut = 0):
    '''
    :param shared_folder: taken from getSharedDirectory()
    :param dataset_uid: taken from dataset.unique_id
    :param model_name: can be for example 'resnet50'
    :param cut: special case scenario, if we were cutting base CNN shorter
    :return:
    '''

    add = ''
    if cut <> 0:
        add = '_cut'+str(cut)

    filename_features_train = shared_folder+'features_train_'+dataset_uid+'_'+model_name+add+'.npy'
    filename_features_test = shared_folder+'features_validation_'+dataset_uid+'_'+model_name+add+'.npy'
    return [filename_features_train, filename_features_test]

# Outputs
def save_visualizations(models, Settings):
    '''
    Save visualizations of the models, if we have set it in Settings
    :param models: list of models to be plotted
    :param Settings: the main Setting, used to access output paths
    :return:
    '''
    index = 0
    for model in models:
        model_settings = Settings["models"][index]
        if model_settings["save_visualization"]:

            # TODO: MODEL_TYPE_SPLIT
            from keras.utils import plot_model

            if model_settings["model_type"] is 'simple_cnn_with_top' or model_settings["model_type"] is 'img_osm_mix':
                #cnn_model = model[0]
                #plot_model(cnn_model, to_file=model_settings["model_image_name"]+'_cnn.png', show_shapes=True)
                top_model = model[1]
                plot_model(top_model, to_file=model_settings["model_shape_filename"], show_shapes=True)

            elif model_settings["model_type"] is 'osm_only':
                plot_model(model[0], to_file=model_settings["model_shape_filename"], show_shapes=True)

            else:
                print "Yet to be programmed."

        index += 1

def save_histories(histories, Settings):
    '''
    Save histories into .npy files, which can be used to reproduce the results.
    :param histories: histories to be saved
    :param Settings: Main setting dict containing the path values
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
    :param histories: histories to be graphed
    :param Settings: Main setting dict containing the path values
    :return:
    '''
    from Downloader.VisualizeHistory import visualize_history, visualize_histories, visualize_special_histories, visualize_whiskered_boxed

    for setting in Settings["graph_histories"]:
        if setting == 'all':
            # graph each of them into their own image
            print 'all'

            index = 0
            for history in histories:
                model_settings = Settings["models"][index]
                graph_file = model_settings["graph_filename"]

                if model_settings["k_fold_crossvalidation"]:
                    continue

                custom_title = 'One:' + model_settings["unique_id"]
                visualize_history(history, show=False, save=True, save_path=graph_file, custom_title=custom_title)
                index +=1

                print "graph saved >>", graph_file

        elif setting == 'together':
            # graph all of them into one image
            print 'together'

            names = []
            index = 0
            histories_selected = []

            for history in histories:
                model_settings = Settings["models"][index]
                if model_settings["k_fold_crossvalidation"]:
                    continue

                custom_name = model_settings["unique_id"]
                names.append(custom_name)
                histories_selected.append(history)
                index +=1

            graph_file = Settings["folders"]["together_graph_filename"]
            custom_title = 'All:' + Settings["folders"]["together_graph_title"]
            visualize_histories(histories_selected, names, plotvalues='loss', show=False, save=True, save_path=graph_file, custom_title=custom_title)
            visualize_histories(histories_selected, names, plotvalues='loss', show=False, save=True, save_path=graph_file+'_justValidation.png', custom_title=custom_title, just_val=True)

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

    model_index = 0
    for special_history in histories:
        model_settings = Settings["models"][model_index]
        if model_settings["k_fold_crossvalidation"]:
            # by default always generate graphs if we used k-fold crossvalidation
            print "Plotting k-fold crossvalidation graphs for model", model_index
            print "from data with", special_history.keys()

            # for whiskered box plots:
            # - best_validation_errors
            # - last_validation_errors
            # - last_training_measure
            # - last_validation_measure
            # - last_training_errors
            # - best_training_measure
            # - best_validation_measure
            # - best_training_errors

            # best_validation_errors, best_training_errors
            data_for_whiskeredboxes = [ special_history["best_training_errors"], special_history["best_validation_errors"] ]
            names = ["best_training_errors", "best_validation_errors"]
            title = 'BestError'

            graph_file = Settings["folders"]["together_graph_filename"] + '_kfoldcrossvalidation_' + title + '.png'
            visualize_whiskered_boxed(data_for_whiskeredboxes, names=names,
                                      show=False, save=True, save_path=graph_file, custom_title=title )

            # best_validation_errors, best_training_errors
            data_for_whiskeredboxes = [ special_history["last_training_errors"], special_history["best_training_errors"],
                                        special_history["last_validation_errors"], special_history["best_validation_errors"] ]
            names = ["last_train", "best_train", "last_val", "best_val"]
            title = 'AllErrors'

            graph_file = Settings["folders"]["together_graph_filename"] + '_kfoldcrossvalidation_AllErrors.png'
            visualize_whiskered_boxed(data_for_whiskeredboxes, names=names,
                                      show=False, save=True, save_path=graph_file, custom_title=title )

            # for a shared graph plot
            # - all_histories_of_this_model
            histories = special_history["all_histories_of_this_model"]
            graph_file = Settings["folders"]["together_graph_filename"] + '_kfoldcrossvalidation' + '.png'
            custom_title = 'k-fold crossvalidation'

            visualize_special_histories(histories, plotvalues='loss', show=False, save=True, save_path=graph_file, custom_title=custom_title)

        model_index += 1

    return 0

def generate_report_string(Settings):
    '''
    Generation of text based report.
    :param Settings: main settings used for the experiment.
    :return:
    '''
    text = ''
    text += ("Experiment [%s] report: \n" % (Settings["experiment_name"]))
    text += ("With %s models: \n" % (len(Settings["models"])))
    for model_settings in Settings["models"]:
        text += ("%s \n" % (model_settings["unique_id"]))
        text += ("%s \n" % (model_settings["model_type"]))
        text += ("Trained for %s epochs with %s optimizer and loss function %s \n" % (model_settings["epochs"], model_settings["optimizer"], model_settings["loss_func"]))
        text += ("Used dataset: %s with %s images \n" % (model_settings["dataset_name"], model_settings["number_of_images"]))

        if model_settings["dump_file_override"] <> '':
            text += ("Dump file used: %s \n" % (model_settings["dump_file_override"]))
        if model_settings["edit_osm_vec"] <> '':
            text += ("OSM vector edited to: %s \n" % (model_settings["edit_osm_vec"]))
        if model_settings["special_case"] <> '':
            text += ("Hacks emplyed: %s \n" % (model_settings["special_case"]))

        text += ("\n")

    return text

def save_report(Settings):
    '''
    Saves report of the most important settings.
    :param Settings:
    :return:
    '''
    with open(Settings["folders"]["report_txt_file"], "w") as text_file:
        text_file.write(generate_report_string(Settings))

    print "report saved >>", Settings["folders"]["report_txt_file"]


def save_models(models, Settings):
    '''
    Saves the trained models alongside with the experiments settings.
    :param models: list of models, each can contain base cnn model or just the top model. We differentiate according
    according to the Settings of model_type.
    :param Settings:
    :return:
    '''

    index = 0
    for model in models:
        model_settings = Settings["models"][index]

        if model_settings["model_type"] is 'simple_cnn_with_top' or model_settings["model_type"] is 'img_osm_mix':
            if model_settings["model_save"] > 0:
                model[1].save(model_settings["model_filename"]+'_top.h5')  # creates a HDF5 file
                print "model saved >>", model_settings["model_filename"]+'_top.h5'
            if model_settings["model_save"] > 1:
                model[0].save(model_settings["model_filename"]+'_cnn.h5')  # creates a HDF5 file
                print "model saved >>", model_settings["model_filename"]+'_cnn.h5'
        elif model_settings["model_type"] is 'osm_only':
            if model_settings["model_save"] > 0:
                model[0].save(model_settings["model_filename"]+'_osmtop.h5')  # creates a HDF5 file
                print "model saved >>", model_settings["model_filename"]+'_osmtop.h5'
        else:
            print "Yet to be programmed."

        index += 1

def load_model(path):
    '''
    Load Keras model from path.
    :param path:
    :return: the loaded model
    '''
    from keras.models import load_model
    return load_model(path)


# Further potentially useful reports

def send_mail_with_graph(Settings):
    '''
    Reporting method by sending mail with graph as an attachment.
    :param Settings:
    :return:
    '''
    subject='Report of Experiment finishing'
    message=generate_report_string(Settings)
    attachment_path=None

    if 'together' in Settings["graph_histories"]:
        attachment_path = Settings["folders"]["together_graph_filename"]

    second_path = ''
    for model_setting in Settings["models"]:
        if model_setting["k_fold_crossvalidation"]:
            graph_file = Settings["folders"]["together_graph_filename"] + '_kfoldcrossvalidation' + '.png'
            second_path = Settings["folders"]["together_graph_filename"] + '_kfoldcrossvalidation_AllErrors.pngAllErrors.png'
            attachment_path = graph_file

    print "## Sending report mail with attachment ", attachment_path
    send_mail(subject, message, attachment_path)

    if second_path <> '':
        send_mail(subject, message, second_path)

def save_metacentrum_report(Settings):
    '''
    Downloads and saves the Metacentrum generated file, according to the unique id value in Settings.
    :param Settings:
    :return:
    '''
    job_id = Settings["job_id"]
    if job_id <> '':
        print "## Downloading ", job_id+'.html'
        save_job_report_page(Settings["folders"]["report_html_file"], job_id)
    else:
        print "## Downloading of job page failed, we don't know job_id", job_id
