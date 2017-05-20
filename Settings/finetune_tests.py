def Setup(Settings,DefaultModel):
    # finetune_tests.py

    Settings["experiment_name"] = "Finetuning-tests"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n = 0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'img_only'
    Settings["models"][n]["epochs"] = 100

    Settings["models"][n]["finetune"] = True
    Settings["models"][n]["finetune_num_of_cnn_layers"] = 9
    Settings["models"][n]["finetune_epochs"] = 5

    return Settings
