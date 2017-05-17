def Setup(Settings,DefaultModel):
    # osm_test_loss_fc.py
    # seems like there is no effect (when comapring mse with mse and mae with mae)

    Settings["experiment_name"] = "Osm_only_test_m squared e-vs-m abs e"

    Settings["graph_histories"] = ['together'] #['all','together',[],[1,0],[0,0,0],[]]

    n=0
    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'mean_absolute_error_as_loss'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 150

    Settings["models"][n]["optimizer"] = 'rmsprop' # 'rmsprop' or 'adam' etc.
    Settings["models"][n]["loss_func"] = 'mean_absolute_error' # 'mean_squared_error' or 'mean_absolute_error' etc.
    Settings["models"][n]["metrics"] = ['mean_squared_error'] # list of 'mean_squared_error' or 'mean_absolute_error' etc.


    Settings["models"].append(DefaultModel.copy())
    n=1

    Settings["models"][n]["model_type"] = 'osm_only'
    Settings["models"][n]["unique_id"] = 'mean_squared_error_as_loss'
    Settings["models"][n]["top_repeat_FC_block"] = 2
    Settings["models"][n]["epochs"] = 150

    Settings["models"][n]["optimizer"] = 'rmsprop' # 'rmsprop' or 'adam' etc.
    Settings["models"][n]["loss_func"] = 'mean_squared_error' # 'mean_squared_error' or 'mean_absolute_error' etc.
    Settings["models"][n]["metrics"] = ['mean_absolute_error'] # list of 'mean_squared_error' or 'mean_absolute_error' etc.


    return Settings
