def Setup(Settings,DefaultModel):
    # shuffle_effective_1200.py

    Settings["experiment_name"] = "Test_Shuffling_3 models vs 3 models"
    Settings["graph_histories"] = ['together', [0,3], [1,4], [2,5],[0,1,2],[3,4,5]]


    n=0
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["model_type"] = 'notShuffled_img_osm_mix'
    Settings["models"][n]["unique_id"] = 'mix'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 300
    Settings["models"][n]["shuffle_dataset"] = False

    Settings["models"].append(DefaultModel.copy())
    n=1
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'notShuffled_osm_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 300
    Settings["models"][n]["shuffle_dataset"] = False


    Settings["models"].append(DefaultModel.copy())
    n=2
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'notShuffled_img_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 300
    Settings["models"][n]["shuffle_dataset"] = False


    Settings["models"].append(DefaultModel.copy())
    n=3
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset

    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'Shuffled_img_osm_mix'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 300
    Settings["models"][n]["shuffle_dataset"] = True

    Settings["models"].append(DefaultModel.copy())
    n=4
    Settings["models"][n]["dataset_pointer"] = 1
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'Shuffled_osm_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 300
    Settings["models"][n]["shuffle_dataset"] = True


    Settings["models"].append(DefaultModel.copy())
    n=5
    Settings["models"][n]["dataset_pointer"] = 1
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'Shuffled_img_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 300
    Settings["models"][n]["shuffle_dataset"] = True



    return Settings
