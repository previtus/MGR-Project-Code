def Setup(Settings,DefaultModel):
    # compare_expanded.py

    Settings["experiment_name"] = "CompareExpandedVsRegular"

    Settings["graph_histories"] = ['together', [0,1], [1,2], [0,2]] #['all','together',[],[1,0],[0,0,0],[]]
    n=0

    # 5556x_reslen30_299px 5556x_reslen20_299px
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'original'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 1000


    Settings["models"].append(DefaultModel.copy())
    n=1

    Settings["models"][n]["dataset_pointer"] = -1 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299_1x_expanded"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables_expanded.dump'
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'expanded'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 1000


    Settings["models"].append(DefaultModel.copy())
    n=2

    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299_1x_agressive_expanded"
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables_expanded.dump'
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["unique_id"] = 'agressively_expanded'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 1000

    return Settings
