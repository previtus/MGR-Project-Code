def Setup(Settings, DefaultModel):
    # kfold_tests.py

    Settings["experiment_name"] = "kfold_tests"

    n = 0
    Settings["models"][n]["model_type"] = 'img_osm_mix' # 'simple_cnn_with_top', 'img_osm_mix', 'osm_only'
    Settings["models"][n]["dataset_name"] = "miniset_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_mark100.dump'
    Settings["models"][n]["pixels"] = 640

    #Settings["models"][n]["dataset_name"] = "1200x_markable_299x299"
    #Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    #Settings["models"][n]["pixels"] = 299

    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'woooottodoowithid'
    Settings["models"][n]["epochs"] = 10


    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 4

    Settings["graph_histories"] = []

    return Settings


