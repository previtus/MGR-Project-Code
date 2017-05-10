def Setup(Settings,DefaultModel):
    Settings["number_of_images"] = 5


    '''
    n = len(Settings["models"])
    Settings["models"].append(DefaultModel.copy())

    Settings["models"][n]["unique_id"] = 'test'
    Settings["models"][n]["finetune_cnn"] = True
    '''

    return Settings
