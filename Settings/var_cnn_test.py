def Setup(Settings,DefaultModel):
    # var_cnn_test.py
    
    Settings["experiment_name"] = "Comparison_of_CNNs_used"

    Settings["graph_histories"] = ['together', [0,1], [1,4], [2,3]] #['all','together',[],[1,0],[0,0,0],[]]

    Settings["models"][0]["model_type"] = 'img_osm_mix'
    Settings["models"][0]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][0]["cnn_model"] = 'resnet50'
    Settings["models"][0]["unique_id"] = 'resnet50_cnn'
    Settings["models"][0]["top_repeat_FC_block"] = 2
    Settings["models"][0]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][0]["epochs"] = 500

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][1]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][1]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][1]["cnn_model"] = 'inception_v3'
    Settings["models"][1]["unique_id"] = 'inception_v3_cnn'
    Settings["models"][1]["top_repeat_FC_block"] = 2
    Settings["models"][1]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][1]["epochs"] = 500

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][2]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][2]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][2]["cnn_model"] = 'vgg19'
    Settings["models"][2]["unique_id"] = 'vgg19_cnn'
    Settings["models"][2]["top_repeat_FC_block"] = 2
    Settings["models"][2]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][2]["epochs"] = 500

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][3]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][3]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][3]["cnn_model"] = 'vgg16'
    Settings["models"][3]["unique_id"] = 'vgg16_cnn'
    Settings["models"][3]["top_repeat_FC_block"] = 2
    Settings["models"][3]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][3]["epochs"] = 500

    Settings["models"].append(DefaultModel.copy())

    Settings["models"][4]["dataset_pointer"] = 0 # 0 - reuse the first dataset
    Settings["models"][4]["dataset_name"] = "5556x_mark_res_299x299"
    Settings["models"][4]["cnn_model"] = 'xception'
    Settings["models"][4]["unique_id"] = 'xception_cnn'
    Settings["models"][4]["top_repeat_FC_block"] = 2
    Settings["models"][4]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][4]["epochs"] = 500

    # main point of this is to cook all those feature files...
    return Settings
