def Setup(Settings,DefaultModel):
    # osm_effect_of_diff_radius_1200ds.py

    Settings["experiment_name"] = "Osm_only_models_radius_effect_1200x"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n=0
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'r50'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R50_4Tables.dump'

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'r100'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'r200'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R200_4Tables.dump'



    return Settings
