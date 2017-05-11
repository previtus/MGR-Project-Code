
def load_default_settings():

    DefaultSettings = {}

    # dataset settings
    DefaultSettings["dataset_name"] = "1200x_markable_299x299"
    DefaultSettings["pixels"] = 299
    DefaultSettings["number_of_images"] = 10
    DefaultSettings["seed"] = 42
    DefaultSettings["validation_split"] = 0.25

    DefaultSettings["models"] = []

    DefaultModel = {}
    DefaultModel["unique_id"] = 'resnet50_top3FC_top150ep_10imgs_299px'
    DefaultModel["cnn_model"] = 'resnet50'
    DefaultModel["cooking_method"] = 'direct' # 'direct' or 'generators'
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

    DefaultSettings["models"].append(DefaultModel)

    DefaultSettings["graph_histories"] = ['all',[]] #['all',[],[0,2]]

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


def load_settings_from_file(file=None, verbose=False):
    Settings, DefaultModel = load_default_settings()

    import os.path
    if file is not None:
        if os.path.isfile(file):
            import imp
            foo = imp.load_source('Setup', file)
            Settings = foo.Setup(Settings,DefaultModel)
        else:
            print "Couldn't find Settings file '", file, "' using the Default Settings instead"

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
