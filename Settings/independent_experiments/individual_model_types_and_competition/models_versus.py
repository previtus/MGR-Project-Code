def Setup(Settings,DefaultModel):
    # models_versus.py

    Settings["experiment_name"] = "TestAllModelsWithThisDataset"

    Settings["graph_histories"] = ['together', [0,1], [1,2], [0,2]] #['all','together',[],[1,0],[0,0,0],[]]
    n=0

    # 5556x_reslen30_299px 5556x_reslen20_299px
    Settings["models"][n]["dataset_name"] = "5556x_reslen30_299px" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'mix'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 20
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'


    Settings["models"].append(DefaultModel.copy())
    n=1

    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'osm_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 20


    Settings["models"].append(DefaultModel.copy())
    n=2

    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'img_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 20

    return Settings
