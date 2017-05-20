def Setup(Settings,DefaultModel):
    # finetune_tests_varA.py

    Settings["experiment_name"] = "Finetuning-tests_big_cca_10hrs_experiment_1k50_varA-useFeat-162"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n = 0
    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["unique_id"] = '1k50_varA-useFeat-162'
    Settings["models"][n]["epochs"] = 1000

    Settings["models"][n]["number_of_images"] = None
    Settings["models"][n]["cooking_method"] = 'generators'

    Settings["models"][n]["finetune"] = True
    Settings["models"][n]["finetune_num_of_cnn_layers"] = 162
    Settings["models"][n]["finetune_epochs"] = 50
    Settings["models"][n]["finetune_DEBUG_METHOD_OF_MODEL_GEN"] = True
    # 5 cca 1 hour
    # 50 cca 10 hrs?

    '''
    16 <keras.layers.merge.Add object at 0x7f5517c4ed50>
    26 <keras.layers.merge.Add object at 0x7f55179e3710>
    36 <keras.layers.merge.Add object at 0x7f5514a647d0>
    48 <keras.layers.merge.Add object at 0x7f5514867d50>
    58 <keras.layers.merge.Add object at 0x7f5514746710>
    68 <keras.layers.merge.Add object at 0x7f55145c97d0>
    78 <keras.layers.merge.Add object at 0x7f5514449890>
    90 <keras.layers.merge.Add object at 0x7f551424ce10>
    100 <keras.layers.merge.Add object at 0x7f551404e7d0>
    110 <keras.layers.merge.Add object at 0x7f5513ecf890>
    120 <keras.layers.merge.Add object at 0x7f5513d53850>
    130 <keras.layers.merge.Add object at 0x7f5513bd3910>
    140 <keras.layers.merge.Add object at 0x7f5513a599d0>
    152 <keras.layers.merge.Add object at 0x7f551385cfd0>
    162 <keras.layers.merge.Add object at 0x7f55136e0910>
    172 <keras.layers.merge.Add object at 0x7f55135639d0>
    '''

    return Settings
