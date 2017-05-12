def Setup(Settings,DefaultModel):
    Settings["experiment_name"] = "DatasetTest-1200x-vs-5556x"


    Settings["models"][0]["dataset_name"] = "1200x_markable_299x299"

    Settings["models"][0]["number_of_images"] = None
    Settings["models"][0]["epochs"] = 150
    Settings["models"][0]["unique_id"] = '1200x'

    n = len(Settings["models"])
    Settings["models"].append(DefaultModel.copy())

    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][0]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["number_of_images"] = None

    Settings["models"][n]["unique_id"] = '5556x'
    Settings["models"][n]["epochs"] = 150
    #Settings["models"][n]["optimizer"] = 'adam'

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]


    return Settings
