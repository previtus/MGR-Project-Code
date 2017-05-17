def Setup(Settings,DefaultModel):
    # simple_hack.py
    Settings["experiment_name"] = "Simple fast model test"

    Settings["graph_histories"] = ['together']

    Settings["models"][0]["model_type"] = 'img_osm_mix'
    Settings["models"][0]["unique_id"] = 'test'
    Settings["models"][0]["top_repeat_FC_block"] = 2
    Settings["models"][0]["epochs"] = 20
    Settings["models"][0]["number_of_images"] = 20

    Settings["models"][0]["special_case"] = 'hack_dont_use_features'
    #Settings["models"][0]["special_case"] = ''

    Settings["experiment_name"] = "Simple fast model test" + str(Settings["models"][0]["number_of_images"]) + " images " + str(Settings["models"][0]["epochs"]) + " epochs_" + Settings["models"][0]["special_case"]

    return Settings
