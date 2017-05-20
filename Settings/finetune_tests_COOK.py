def Setup(Settings,DefaultModel):
    # finetune_tests_COOK.py

    Settings["experiment_name"] = "Finetuning-tests_big_cca_10hrs_experiment_COOK"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n = 0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'img_only'
    Settings["models"][n]["epochs"] = 2

    Settings["models"][n]["number_of_images"] = None
    Settings["models"][n]["cooking_method"] = 'generators'
    # COOK ALL THE FINETUNING FEATURES

    Settings["models"][n]["finetune"] = True
    Settings["models"][n]["finetune_num_of_cnn_layers"] = 162
    Settings["models"][n]["finetune_epochs"] = 0

    Settings["models"][n]["number_of_images"] = None
    Settings["models"][n]["cooking_method"] = 'generators'


    Settings["models"].append(DefaultModel.copy())
    n+=1
    Settings["models"][n]["dataset_name"] = "1200x_markable_299x299"
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'b'
    Settings["models"][n]["epochs"] = 2

    Settings["models"][n]["finetune"] = True
    Settings["models"][n]["finetune_num_of_cnn_layers"] = 152
    Settings["models"][n]["finetune_epochs"] = 0

    Settings["models"][n]["number_of_images"] = None
    Settings["models"][n]["cooking_method"] = 'generators'

    return Settings
