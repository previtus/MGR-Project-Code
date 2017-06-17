def Setup(Settings,DefaultModel):
    # minimal_model.py

    Settings["experiment_name"] = "minimalModel"
    Settings["models"][0]["dataset_name"] = "5556x_reslen20_299px"
    Settings["models"][0]["epochs"] = 5

    return Settings
