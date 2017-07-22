def Setup(Settings,DefaultModel):
    # osm_test_log_osm.py

    Settings["experiment_name"] = "Osm_only_models-data-edits"
    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]


    n=0
    Settings["models"][n]["dataset_name"] = "5556x_reslen20_299px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'osm_only' # 'simple_cnn_with_top', 'img_osm_mix', 'osm_only'
    Settings["models"][n]["unique_id"] = 'clean'
    Settings["models"][n]["epochs"] = 1000
    Settings["models"][n]["edit_osm_vec"] = ''


    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1
    Settings["models"][n]["dataset_name"] = "5556x_reslen20_299px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'osm_only' # 'simple_cnn_with_top', 'img_osm_mix', 'osm_only'
    Settings["models"][n]["unique_id"] = 'log_data'
    Settings["models"][n]["epochs"] = 1000
    Settings["models"][n]["edit_osm_vec"] = 'log'

    return Settings
