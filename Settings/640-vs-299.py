def Setup(Settings,DefaultModel):
    # 640-vs-299.py
    # The results of 1200x vs 5556x in the case of simple_cnn_with_top is basically no change

    Settings["experiment_name"] = "DatasetTest-640-vs-299"


    Settings["models"][0]["dataset_name"] = "5556x_mark_res_299x299"

    Settings["models"][0]["number_of_images"] = None
    Settings["models"][0]["epochs"] = 100
    Settings["models"][0]["unique_id"] = '299px'

    n = len(Settings["models"])
    Settings["models"].append(DefaultModel.copy())

    Settings["models"][1]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][1]["dataset_name"] = "5556x_markable_640x640"
    Settings["models"][1]["number_of_images"] = None

    Settings["models"][1]["unique_id"] = '640px'
    Settings["models"][1]["pixels"] = 640

    Settings["models"][1]["epochs"] = 100
    #Settings["models"][1]["optimizer"] = 'adam'

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]


    return Settings
