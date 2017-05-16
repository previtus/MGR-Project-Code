def Setup(Settings,DefaultModel):
    # osm_only_model.py

    Settings["experiment_name"] = "Osm_only_models"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    Settings["models"][0]["model_type"] = 'osm_only'
    Settings["models"][0]["unique_id"] = '1fc'
    Settings["models"][0]["top_repeat_FC_block"] = 1
    Settings["models"][0]["epochs"] = 300

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][1]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][1]["model_type"] = 'osm_only'
    Settings["models"][1]["unique_id"] = '2fc'
    Settings["models"][1]["top_repeat_FC_block"] = 2
    Settings["models"][1]["epochs"] = 300

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][2]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][2]["model_type"] = 'osm_only'
    Settings["models"][2]["unique_id"] = '3fc'
    Settings["models"][2]["top_repeat_FC_block"] = 3
    Settings["models"][2]["epochs"] = 300

    return Settings
