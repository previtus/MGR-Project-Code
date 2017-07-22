def Setup(Settings,DefaultModel):
    # set6_variable-base-cnn-model/var_cnn_test_proper_dataset_xception_kfold299.py
    
    Settings["experiment_name"] = "var_cnn_test_proper_dataset_xception_kfold299"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]
    Settings["report_on_models"] = True

    n=0
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'xception'
    Settings["models"][n]["unique_id"] = 'xception_cnn'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'img_osm_mix'

    Settings["models"][n]["epochs"] = 100

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 4

    Settings["graph_histories"] = []

    return Settings
