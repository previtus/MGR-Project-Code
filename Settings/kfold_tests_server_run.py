def Setup(Settings, DefaultModel):
    # kfold_tests_server_run.py

    Settings["experiment_name"] = "kfold_tests_bigDataset"

    n = 0
    Settings["models"][n]["model_type"] = 'img_osm_mix' # 'simple_cnn_with_top', 'img_osm_mix', 'osm_only'
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640

    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'bigDataset'
    Settings["models"][n]["epochs"] = 500

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 10

    Settings["graph_histories"] = []

    return Settings


