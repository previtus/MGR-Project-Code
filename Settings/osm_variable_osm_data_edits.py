def Setup(Settings,DefaultModel):
    # osm_variable_osm_data_edits.py
    #

    Settings["experiment_name"] = "Osm_only_models-data-edits"
    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]


    n=0
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'

    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'from4tables_better_data_maybe'
    Settings["models"][n]["epochs"] = 2000
    Settings["models"][n]["edit_osm_vec"] = ''


    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["dump_file_override"] = ''

    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'from1table'
    Settings["models"][n]["epochs"] = 2000
    Settings["models"][n]["edit_osm_vec"] = ''

    return Settings
