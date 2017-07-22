def Setup(Settings,DefaultModel):
    # osm_only_variable_width.py

    Settings["experiment_name"] = "Osm_o_variable_width"

    Settings["graph_histories"] = ['together', [0,1], [0,2], [0,3]] #['all','together',[],[1,0],[0,0,0],[]]

    n=0
    Settings["models"][n]["dataset_name"] = "5556x_markable_640x640" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'normal_width_2x256'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 1000
    Settings["models"][n]["osm_manual_width"] = 256
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'


    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = 0
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'thin_2x32'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 1000
    Settings["models"][n]["osm_manual_width"] = 32


    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'superthin_3x8'
    Settings["models"][n]["top_repeat_FC_block"] = 3
    Settings["models"][n]["epochs"] = 1000
    Settings["models"][n]["osm_manual_width"] = 8

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'med_2x64'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 1000
    Settings["models"][n]["osm_manual_width"] = 64


    return Settings
