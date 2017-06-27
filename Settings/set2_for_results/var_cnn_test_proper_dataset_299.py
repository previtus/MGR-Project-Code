def Setup(Settings,DefaultModel):
    # set2_for_results/var_cnn_test_proper_dataset.py
    
    Settings["experiment_name"] = "Comparison_of_CNNs_on_5556x_640"

    Settings["graph_histories"] = ['together', [0,1], [1,4], [2,3]] #['all','together',[],[1,0],[0,0,0],[]]

    Settings["report_on_models"] = True
    n=0
    Settings["models"][n]["model_type"] = 'img_osm_mix'
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_cnn'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 2
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'

    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'inception_v3'
    Settings["models"][n]["unique_id"] = 'inception_v3_cnn'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 2
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'img_osm_mix'

    Settings["models"].append(DefaultModel.copy())
    n += 1
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'vgg19'
    Settings["models"][n]["unique_id"] = 'vgg19_cnn'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 2
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'img_osm_mix'

    Settings["models"].append(DefaultModel.copy())
    n += 1
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'vgg16'
    Settings["models"][n]["unique_id"] = 'vgg16_cnn'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 2
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'img_osm_mix'

    Settings["models"].append(DefaultModel.copy())
    n += 1
    Settings["models"][n]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][n]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][n]["pixels"] = 299
    Settings["models"][n]["cnn_model"] = 'xception'
    Settings["models"][n]["unique_id"] = 'xception_cnn'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 2
    Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["model_type"] = 'img_osm_mix'

    # main point of this is to cook all those feature files...
    return Settings
