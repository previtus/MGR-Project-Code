def Setup(Settings,DefaultModel):
    # osm_only_model.py
    # Ps: edit_osm_vec 'booleans' has worse results

    Settings["experiment_name"] = "Osm_only_models"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n=0
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = '2fc_Cats'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500
    Settings["models"][n]["edit_osm_vec"] = 'low-mid-high'

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = 0
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = '3fc_Cats'
    Settings["models"][n]["top_repeat_FC_block"] = 3
    Settings["models"][n]["epochs"] = 500
    Settings["models"][n]["edit_osm_vec"] = 'low-mid-high'

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = '2fc_boolTrans'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500
    Settings["models"][n]["edit_osm_vec"] = 'booleans'

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = '2fc_normal'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500
    Settings["models"][n]["edit_osm_vec"] = ''

    return Settings
