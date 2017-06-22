def Setup(Settings,DefaultModel):
    # set6/var_cnn_test_proper_dataset_inception_v3.py
    
    Settings["experiment_name"] = "var_cnn_test_proper_dataset_inception_v3_kfold"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n=0
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_markable_640x640"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'inception_v3'
    Settings["models"][n]["unique_id"] = 'inception_v3_cnn'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'img_osm_mix'

    Settings["models"][n]["epochs"] = 500

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 10

    Settings["graph_histories"] = []

    return Settings