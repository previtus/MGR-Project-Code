def Setup(Settings,DefaultModel):
    # compare_expanded_kfold_a.py

    Settings["experiment_name"] = "CompareExpandedVsRegular_kfold_original"

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

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 10

    Settings["graph_histories"] = []

    return Settings
