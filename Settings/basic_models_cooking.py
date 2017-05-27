def Setup(Settings,DefaultModel):
    # basic_models_cooking.py
    
    Settings["experiment_name"] = "BasicModelCookingShow"

    Settings["graph_histories"] = ['together']
    # it's not about the results, but about the journey!

    # we are interested in ResNet50
    # and these datasets
    # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"

    # will cook them into this:
    ''' with current seed
        shared/features_train_1200x_markable_299x299299-full-seed13_resnet50.npy
        shared/features_train_5556x_mark_res_299x299299-full-seed13_resnet50.npy
        shared/features_train_5556x_markable_640x640640-full-seed13_resnet50.npy
        shared/features_validation_1200x_markable_299x299299-full-seed13_resnet50.npy
        shared/features_validation_5556x_mark_res_299x299299-full-seed13_resnet50.npy
        shared/features_validation_5556x_markable_640x640640-full-seed13_resnet50.npy
    '''

    n=0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_reslen30_299px"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_reslen30_299px'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5

    Settings["models"].append(DefaultModel.copy())
    n=1
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_reslen20_299px"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_reslen20_299px'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5

    Settings["models"].append(DefaultModel.copy())
    n=2
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_minlen30_640px'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5

    Settings["models"].append(DefaultModel.copy())
    n=3
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_minlen20_640px"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_minlen20_640px'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5


    '''
    n=0
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_1200x_markable_299x299'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5

    Settings["models"].append(DefaultModel.copy())
    n=1
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_mark_res_299x299'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5

    Settings["models"].append(DefaultModel.copy())
    n=2
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_markable_640x640"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_markable_640x640'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5
    '''

    return Settings
