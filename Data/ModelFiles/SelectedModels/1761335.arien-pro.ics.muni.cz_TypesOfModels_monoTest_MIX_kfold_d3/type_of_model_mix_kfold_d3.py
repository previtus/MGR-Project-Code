def Setup(Settings, DefaultModel):
    # set3_crossval-one-model-on-one-dataset/type_of_model_mix_kfold_d3.py

    Settings["experiment_name"] = "TypesOfModels_monoTest_MIX_kfold_d3"

    Settings["graph_histories"] = []  # ['all','together',[],[1,0],[0,0,0],[]]
    n = 0

    #d1 5556x_markable_640x640                SegmentsData_marked_R100_4Tables
    #d2 5556x_markable_640x640_2x_expanded    SegmentsData_marked_R100_4Tables_expanded.dump
    #d3 5556x_minlen30_640px                  SegmentsData_marked_R100_4Tables.dump
    #d4 5556x_minlen30_640px_2x_expanded      SegmentsData_marked_R100_4Tables_expanded.dump
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'img_osm_mix' # osm_only img_only img_osm_mix
    Settings["models"][n]["unique_id"] = 'mixmodel'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 10

    Settings["graph_histories"] = []

    return Settings
