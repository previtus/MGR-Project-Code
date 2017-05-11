def Setup(Settings,DefaultModel):
    Settings["number_of_images"] = 500
    Settings["models"][0]["epochs"] = 20
    Settings["models"][0]["cooking_method"] = 'generators' # 'direct' or 'generators'


    '''
    n = len(Settings["models"])
    Settings["models"].append(DefaultModel.copy())

    Settings["models"][n]["unique_id"] = 'test'
    Settings["models"][n]["finetune_cnn"] = True
    '''

    return Settings
