def Setup(Settings,DefaultModel):
    # noncanon_dataset.py

    # we will basically take an existing dataset, generate small changes of it
    # into a temporary dictionary Logs/Temp/<dataset_name>
    # there we will have all the images and fresh new segments file
    # cooking of feature file is possible, but into Logs/Temp/<dataset_name>/features..

    # folder structure:
    # Logs/Temp/<dataset_name>/
    #   - images
    #   - SegmentsData.dump / SegmentsData_marked_R100.dump
    #   - features_train...npy
    #   - features_valid...npy

    Settings["experiment_name"] = "NonCanonDataset"

    Settings["graph_histories"] = ['together']

    n=0
    Settings["models"][n]["noncanon_dataset"] = 'expand_existing_dataset'



    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "5556x_minlen30_640px"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'resnet50_5556x_minlen30_640px'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5
    #Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'

    return Settings
