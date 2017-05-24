import DatasetHandler.CreateDataset
from Omnipresent import len_

def get_dataset():
    model_settings = {}
    model_settings["dataset_name"] = "1200x_markable_299x299"
    model_settings["pixels"] = 299
    model_settings["number_of_images"] = None
    model_settings["seed"] = 13
    model_settings["validation_split"] = 0.25
    model_settings["dump_file_override"] = ''

    dataset = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                                                       desired_number=model_settings["number_of_images"],
                                                       seed=model_settings["seed"],
                                                       filename_override=model_settings["dump_file_override"])

    [osm, osm_val] = dataset.getDataLabels_split_only_osm(validation_split=model_settings["validation_split"])
    [y, y_val] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])

    print len_(y), len_(y_val), len_(osm), len_(osm_val)
    return dataset, osm, osm_val, y, y_val
