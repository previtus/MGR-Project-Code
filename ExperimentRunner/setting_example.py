def Setup(Settings,DefaultModel):
    Settings["dataset_name"] = 'foo'

    Settings["seed"] = 20

    n = len(Settings["models"])
    Settings["models"].append(DefaultModel.copy())

    Settings["models"][n]["unique_id"] = 'test'
    Settings["models"][n]["finetune_cnn"] = True

    Settings["graph_histories"] = ['all',[0]]

    return Settings
