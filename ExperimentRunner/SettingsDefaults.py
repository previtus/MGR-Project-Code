
def load_default_settings():
    '''
    Default setting definition.
    :return: Default setting for whole experiment and for first model in dictionaries.
    '''

    DefaultSettings = {}

    # dataset settings
    DefaultSettings["experiment_name"] = "basic"
    DefaultSettings["interrupt"] = False
    DefaultSettings["report_on_models"] = False
    DefaultSettings["models"] = []

    DefaultModel = {}

    # dataset setting
    DefaultModel["dataset_pointer"] = -1 # if = -1, then create new dataset, otherwise use dataset of model of this index
    DefaultModel["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    DefaultModel["dump_file_override"] = '' # '' is default, could also be 'SegmentsData_marked_R100_4Tables.dump' ... etc
    DefaultModel["pixels"] = 299
    DefaultModel["number_of_images"] = None
    DefaultModel["seed"] = 13
    DefaultModel["validation_split"] = 0.25

    DefaultModel["unique_id"] = 'resnet50_top3FC_top150ep_10imgs_299px'
    DefaultModel["cnn_model"] = 'resnet50'
    DefaultModel["cooking_method"] = 'generators' # 'direct' or 'generators'
    DefaultModel["cut_cnn"] = 0
    DefaultModel["model_type"] = 'simple_cnn_with_top' # 'simple_cnn_with_top', 'img_osm_mix', 'osm_only'
    DefaultModel["top_repeat_FC_block"] = 3
    DefaultModel["save_visualization"] = True

    # Train and Test specifics
    DefaultModel["epochs"] = 150
    DefaultModel["optimizer"] = 'rmsprop' # 'rmsprop' or 'adam' etc.
    DefaultModel["loss_func"] = 'mean_squared_error' # 'mean_squared_error' or 'mean_absolute_error' etc.
    DefaultModel["metrics"] = ['mean_absolute_error'] # list of 'mean_squared_error' or 'mean_absolute_error' etc.
    DefaultModel["train_top"] = True # Always True??
    DefaultModel["test_existence_of_images"] = True
    DefaultModel["evaluation_after_training"] = False

    DefaultModel["k_fold_crossvalidation"] = False
    DefaultModel["crossvalidation_k"] = 4

    DefaultModel["finetune"] = False
    from keras import optimizers
    DefaultModel["finetune_optimizer"] = optimizers.SGD(lr=1e-4, momentum=0.9)
    DefaultModel["finetune_num_of_cnn_layers"] = 5
    DefaultModel["finetune_epochs"] = 5

    DefaultModel["finetune_DEBUG_METHOD_OF_MODEL_GEN"] = True # True - uses cooked feature files, False - trains the whole model on spot

    # Hurray for shuffling
    DefaultModel["shuffle_dataset"] = True
    DefaultModel["shuffle_dataset_method"] = 'default-same-segment'

    # OSM data editation
    DefaultModel["edit_osm_vec"] = '' # 'booleans', 'low-mid-high'

    DefaultModel["osm_manual_width"] = 256

    # Special case HACKS
    DefaultModel["special_case"] = '' # by default no hack # hack_dont_use_features, is not yet prepared
    DefaultModel["osm_only_unique_osms"] = False

    # Noncanon dataset creation
    DefaultModel["noncanon_dataset"] = '' # can be 'expand_existing_dataset'


    DefaultSettings["models"].append(DefaultModel)
    DefaultSettings["graph_histories"] = ['all','together',[]] #['all',[],[0,2]]

    # empty values, which will be filled:
    DefaultSettings["filename_features_train"] = ''
    DefaultSettings["filename_features_test"] = ''
    DefaultSettings["finetune_features_train"] = ''
    DefaultSettings["finetune_features_test"] = ''

    return DefaultSettings, DefaultModel

def print_settings(Settings, ignore_default_values = True):
    '''
    Debug of Settings, prints values which are not like the ones in Default setting file.
    :param Settings: Custom setting to be checked
    :param ignore_default_values: Flag to ignore default values (for better clarity)
    :return:
    '''
    print "## Loaded Settings:"
    t = ' '
    DefaultSettings, DefaultModel = load_default_settings()
    for key in Settings.keys():
        if key is not 'models':
            if not ignore_default_values or not Settings[key] == DefaultSettings[key]:
                print t,key, '=', Settings[key]

    for model in Settings["models"]:
        print t,"[model]", model["unique_id"]
        for subkey in model.keys():
            if not ignore_default_values or not model[subkey] == DefaultModel[subkey]:
                print t,t,subkey, model[subkey]


def load_settings_from_file(file=None, job_id='', verbose=False):
    '''
    Load Settings from a custom settings description file.
    :param file: Load from file
    :param job_id: Unique id
    :param verbose: Flag to debug info about loaded Settings
    :return: Settings dictionary
    '''
    print "## Job: ", job_id," Loading Settings from ",file

    Settings, DefaultModel = load_default_settings()
    Settings["job_id"] = job_id

    import os.path
    if file is not None:
        if os.path.isfile(file):
            import imp
            foo = imp.load_source('Setup', file)
            Settings = foo.Setup(Settings,DefaultModel)
        else:
            print "Couldn't find Settings file '", file, "' using the Default Settings instead"
            Settings["interrupt"] = True

    if verbose:
        print_settings(Settings, ignore_default_values=True)

    return Settings

    ## Typical usage example
    #load_settings_from_file('setting_example.py', verbose=True)
    # EXAMPLE OF SETTINGS FILE <setting_example.py>:
    '''
    
    def Setup(Settings,DefaultModel):
        Settings["dataset_name"] = 'foo'
    
        Settings["seed"] = 20
    
        n = len(Settings["models"])
        Settings["models"].append(DefaultModel.copy())
    
        Settings["models"][n]["unique_id"] = 'test'
        Settings["models"][n]["finetune_cnn"] = True
    
        Settings["graph_histories"] = ['all',[0]]
    
        return Settings
    
    '''
