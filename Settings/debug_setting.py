def Setup(Settings, DefaultModel):
    # debug_setting.py

    Settings["experiment_name"] = "debug"

    Settings["graph_histories"] = ['together']

    n = 0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["dataset_name"] = "5556x_markable_640x640"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'aaaa'
    Settings["models"][n]["dump_file_override"] = 'SegmentsData.dump'
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["epochs"] = 5
    Settings["models"][n]["test_existence_of_images"] = False

    Settings["models"][n]["special_case"] = 'debug'


    return Settings
