
def load_default_settings():

    DefaultSettings = {}

    # dataset settings
    DefaultSettings["experiment_name"] = "basic"
    DefaultSettings["interrupt"] = False
    DefaultSettings["models"] = []

    DefaultModel = {}

    # dataset setting
    DefaultModel["dataset_pointer"] = -1 # if = -1, then create new dataset, otherwise use dataset of model of this index
    DefaultModel["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    DefaultModel["pixels"] = 299
    DefaultModel["number_of_images"] = None
    DefaultModel["seed"] = 13
    DefaultModel["validation_split"] = 0.25

    DefaultModel["unique_id"] = 'resnet50_top3FC_top150ep_10imgs_299px'
    DefaultModel["cnn_model"] = 'resnet50'
    DefaultModel["cooking_method"] = 'generators' # 'direct' or 'generators'
    DefaultModel["cut_cnn"] = 0
    DefaultModel["model_type"] = 'simple_cnn_with_top'
    DefaultModel["top_repeat_FC_block"] = 3
    DefaultModel["save_visualization"] = True

    # Train and Test specifics
    DefaultModel["epochs"] = 150
    DefaultModel["optimizer"] = 'rmsprop' # 'rmsprop' or 'adam' etc.
    DefaultModel["loss_func"] = 'mean_squared_error' # 'mean_squared_error' or 'mean_absolute_error' etc.
    DefaultModel["metrics"] = ['mean_absolute_error'] # list of 'mean_squared_error' or 'mean_absolute_error' etc.
    DefaultModel["train_top"] = True
    DefaultModel["finetune_cnn"] = False
    DefaultModel["finetune_cnn_last"] = 10
    DefaultModel["finetune_all"] = False
    DefaultModel["finetune_all_last"] = 10

    # Hurray for shuffling
    DefaultModel["shuffle_dataset"] = True

    # OSM data editation
    DefaultModel["edit_osm_vec"] = '' # 'booleans', 'low-mid-high'

    # Special case HACKS
    DefaultModel["special_case"] = '' # by default no hack # hack_dont_use_features, is not yet prepared

    DefaultSettings["models"].append(DefaultModel)

    DefaultSettings["graph_histories"] = ['all','together',[]] #['all',[],[0,2]]

    return DefaultSettings, DefaultModel

def print_settings(Settings, ignore_default_values = True):
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
