def Setup(Settings,DefaultModel):
    # finetune_tests.py

    Settings["experiment_name"] = "Finetuning-tests_big_cca_10hrs_experiment_FixedN"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n = 0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = 'img_only'
    Settings["models"][n]["epochs"] = 1000

    Settings["models"][n]["finetune"] = True
    Settings["models"][n]["finetune_num_of_cnn_layers"] = 9
    Settings["models"][n]["finetune_epochs"] = 50
    # 5 cca 1 hour
    # 50 cca 10 hrs?

    return Settings
