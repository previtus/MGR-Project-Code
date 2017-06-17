def Setup(Settings, DefaultModel):
    # kfold_tests.py

    Settings["experiment_name"] = "kfold_tests"

    n = 0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "miniset_640px"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'woooottodoowithid'
    Settings["models"][n]["epochs"] = 5

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 4

    return Settings


