def Setup(Settings,DefaultModel):
    # osm_only_test_det_mixing.py


    Settings["experiment_name"] = "Osm_only_models_compare_det_mixing"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n=0
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'same_segment'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 50

    Settings["models"][n]["special_case"] == 'same_segment'


    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = 0
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'modulo'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 50

    Settings["models"][n]["special_case"] == 'modulo'


    return Settings
