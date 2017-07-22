def Setup(Settings,DefaultModel):
    # set1-test_of_models_against_datasets/models_30m_640px.py

    Settings["experiment_name"] = "set1c_Models_Test_30m_640px"

    Settings["graph_histories"] = ['together', [0,1], [1,2], [0,2]]
    n=0

    # 5556x_minlen30_640px 5556x_minlen20_640px 5556x_reslen20_299px 5556x_reslen30_299px
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'mix'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 800
    # c
    Settings["models"][n]["loss_func"] = 'mean_absolute_error'
    Settings["models"][n]["metrics"] = ['mean_squared_error']

    Settings["models"].append(DefaultModel.copy())
    n=1

    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'osm_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 800
    # c
    Settings["models"][n]["loss_func"] = 'mean_absolute_error'
    Settings["models"][n]["metrics"] = ['mean_squared_error']


    Settings["models"].append(DefaultModel.copy())
    n=2

    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'img_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 800
    # c
    Settings["models"][n]["loss_func"] = 'mean_absolute_error'
    Settings["models"][n]["metrics"] = ['mean_squared_error']


    return Settings
