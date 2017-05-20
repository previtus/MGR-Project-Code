def Setup(Settings,DefaultModel):
    # manual_model.py

    Settings["experiment_name"] = "Manual_model_def"

    Settings["graph_histories"] = ['together']

    n = 0
    Settings["models"][n]["model_type"] = 'manual'
    Settings["models"][n]["unique_id"] = 'manual_model'
    Settings["models"][n]["epochs"] = 100

    cnn_model = []
    top_model = []

    return Settings
