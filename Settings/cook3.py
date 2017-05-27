def Setup(Settings,DefaultModel):
    # basic_models_cooking.py
    
    Settings["experiment_name"] = "cook"

    Settings["graph_histories"] = ['together']

    n=0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_minlen30_640px'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5

    return Settings
