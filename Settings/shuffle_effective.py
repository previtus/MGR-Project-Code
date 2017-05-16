def Setup(Settings,DefaultModel):
    # shuffle_effective.py

    Settings["experiment_name"] = "Test_Shuffling"

    Settings["graph_histories"] = ['together', [0,1], [1,2], [0,2]] #['all','together',[],[1,0],[0,0,0],[]]

    Settings["models"][0]["model_type"] = 'img_osm_mix'
    Settings["models"][0]["unique_id"] = 'shuffled'
    Settings["models"][0]["top_repeat_FC_block"] = 2
    Settings["models"][0]["epochs"] = 150
    Settings["models"][0]["shuffle_dataset"] = True

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][1]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][1]["model_type"] = 'img_osm_mix'
    Settings["models"][1]["unique_id"] = 'not-shuffled'
    Settings["models"][1]["top_repeat_FC_block"] = 2
    Settings["models"][1]["epochs"] = 150
    Settings["models"][1]["shuffle_dataset"] = False

    return Settings
