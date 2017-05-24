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

    import numpy as np
    #for i in range(0,10):
    #    print np.sum(osm[i])
    #print y[0:10]

    no_duals_osm = []
    no_duals_y = []

    duals = 0
    for i in range(1,len(y)):
        if (osm[i] == osm[i-1]).all() and y[i]==y[i-1]:
            #print i, ' is the same as ', i-1
            duals += 1
        else:
            no_duals_osm.append(osm[i])
            no_duals_y.append(y[i])

    no_duals_osm_val = []
    no_duals_y_val = []

    duals_val = 0

    for i in range(1,len(y_val)):
        if (osm_val[i] == osm_val[i-1]).all() and y_val[i]==y_val[i-1]:
            #print i, ' is the same as ', i-1
            duals_val += 1
        else:
            no_duals_osm_val.append(osm_val[i])
            no_duals_y_val.append(y_val[i])

    print "Duals:", duals, duals_val

    no_duals_osm = np.asarray(no_duals_osm)
    no_duals_osm_val = np.asarray(no_duals_osm_val)
    no_duals_y = np.asarray(no_duals_y)
    no_duals_y_val = np.asarray(no_duals_y_val)

    return dataset, no_duals_osm, no_duals_osm_val, no_duals_y, no_duals_y_val
    return dataset, osm, osm_val, y, y_val
