def Setup(Settings, DefaultModel):
    # set4a/set4a_MinEdgeSize_img_len20_kfold_d5.py

    Settings["experiment_name"] = "set4a_MinEdgeSize_img_len20_kfold_d5"

    Settings["graph_histories"] = []  # ['all','together',[],[1,0],[0,0,0],[]]
    n = 0

    #d1 5556x_markable_640x640                SegmentsData_marked_R100_4Tables
    #d2 5556x_markable_640x640_2x_expanded    SegmentsData_marked_R100_4Tables_expanded.dump
    #d3 5556x_minlen30_640px                  SegmentsData_marked_R100_4Tables.dump
    #d4 5556x_minlen30_640px_2x_expanded      SegmentsData_marked_R100_4Tables_expanded.dump

    #d5 5556x_minlen10_640px                  SegmentsData_marked_R100_4Tables.dump
    #d6 5556x_minlen20_640px                  SegmentsData_marked_R100_4Tables.dump


    Settings["models"][n]["dataset_name"] = "5556x_minlen20_640px"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top' # osm_only img_only img_osm_mix
    Settings["models"][n]["unique_id"] = 'img_with_min10'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 500

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 10

    Settings["graph_histories"] = []

    return Settings
