def Setup(Settings,DefaultModel):
    Settings["experiment_name"] = "Number_of_FC_blocks_test"


    Settings["models"][0]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][0]["number_of_images"] = None
    Settings["models"][0]["epochs"] = 150
    Settings["models"][0]["unique_id"] = '1fc'
    Settings["models"][0]["top_repeat_FC_block"] = 1

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][1]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][1]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][1]["number_of_images"] = None
    Settings["models"][1]["epochs"] = 150
    Settings["models"][1]["unique_id"] = '2fc'
    Settings["models"][1]["top_repeat_FC_block"] = 2

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][2]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][2]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][2]["number_of_images"] = None
    Settings["models"][2]["epochs"] = 150
    Settings["models"][2]["unique_id"] = '3fc'
    Settings["models"][2]["top_repeat_FC_block"] = 3

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]


    return Settings
