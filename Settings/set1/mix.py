def Setup(Settings,DefaultModel):
    # set1/osm.py

    Settings["experiment_name"] = "set1b_Mix_model_versus_datasets_640px"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    # 5556x_minlen30_640px 5556x_minlen20_640px 5556x_reslen20_299px 5556x_reslen30_299px

    n=0
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'mix_minlen30_640px'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 800

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1
    Settings["models"][n]["dataset_name"] = "5556x_minlen20_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'mix_minlen20_640px'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 800

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1
    Settings["models"][n]["dataset_name"] = "5556x_minlen10_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'mix_minlen10_640px'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 800

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1
    Settings["models"][n]["dataset_name"] = "5556x_markable_640x640"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'mix_nosplit_640px'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 800

    return Settings
