def Setup(Settings, DefaultModel):
    # set5/set5_w256_depth3_d1.py

    Settings["experiment_name"] = "set5_w256_depth3_d1"

    Settings["graph_histories"] = []  # ['all','together',[],[1,0],[0,0,0],[]]
    n = 0

    #d1 5556x_markable_640x640                SegmentsData_marked_R100_4Tables
    #d2 5556x_markable_640x640_2x_expanded    SegmentsData_marked_R100_4Tables_expanded.dump
    #d3 5556x_minlen30_640px                  SegmentsData_marked_R100_4Tables.dump
    #d4 5556x_minlen30_640px_2x_expanded      SegmentsData_marked_R100_4Tables_expanded.dump

    #d5 5556x_minlen10_640px                  SegmentsData_marked_R100_4Tables.dump
    #d6 5556x_minlen20_640px                  SegmentsData_marked_R100_4Tables.dump

    #d7 5556x_mark_res_299x299                SegmentsData_marked_R100_4Tables.dump

    Settings["models"][n]["dataset_name"] = "5556x_markable_640x640"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["model_type"] = 'osm_only' # osm_only simple_cnn_with_top img_osm_mix
    Settings["models"][n]["unique_id"] = 'osm'
    # Depth
    Settings["models"][n]["top_repeat_FC_block"] = 3
    # try 1
    # try 2 =def
    # try 3
    # try 4

    # Width
    Settings["models"][n]["osm_manual_width"] = 256
    # try 32
    # try 64
    # try 128
    # try 256 def
    # dont try 512

    Settings["models"][n]["epochs"] = 1000

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 10

    Settings["graph_histories"] = []

    return Settings
