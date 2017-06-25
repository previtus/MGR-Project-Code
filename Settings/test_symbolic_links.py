def Setup(Settings,DefaultModel):
    # test_symbolic_links.py
    
    Settings["experiment_name"] = "testtesttest_symbolic_links"

    Settings["graph_histories"] = ['together']

    n=0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_markable_640x640_2x_expanded"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["unique_id"] = 'testtesttest'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 2

    return Settings
