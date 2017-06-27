def Setup(Settings,DefaultModel):
    # osm_multiple_radii.py

    Settings["experiment_name"] = "Osm_Multiple_Radii"

    Settings["graph_histories"] = ['together']

    n=0
    Settings["models"][n]["dataset_name"] = "5556x_reslen20_299px" # "1200x_markable_299x299", "5556x_mark_res_299x299", "5556x_markable_640x640"
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'normal_osm_only'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 50
    Settings["models"][n]["edit_osm_vec"] = ''
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'

    return Settings
