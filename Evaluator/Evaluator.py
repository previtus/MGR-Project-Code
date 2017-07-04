import ExperimentRunner.SettingsDefaults as SettingsDefaults

import ModelHandler.ModelOI as ModelOI
import ModelHandler.ModelGenerator as ModelGenerator
import ModelHandler.ModelTester as ModelTester
import DatasetHandler as DatasetHandler
from Omnipresent import len_


def evaluator_load_model(model_file, settings_file, verbose=False):
    ### LOAD skeleton of model and dataset
    Settings = SettingsDefaults.load_settings_from_file(settings_file, '', verbose=False)
    if verbose:
        print Settings

    Settings["models"][0]["test_existence_of_images"] = False
    Settings["models"][0]["evaluation_after_training"] = True
    Settings["models"][0]["model_shape_filename"] = "tmp.png"
    model_settings = Settings["models"][0]

    models = ModelGenerator.get_cnn_models(Settings)
    models = ModelGenerator.get_top_models(models, None, Settings)

    if Settings["interrupt"]:
        return 365
    if Settings["report_on_models"]:
        ModelGenerator.report_models(models, Settings)

    if verbose:
        ModelOI.save_visualizations(models, Settings)

    ### WEIGHTS to model from file
    if verbose:
        print len(models), model_file

    loaded_model = models[0]
    if model_settings["model_type"] is 'osm_only':
        # osm model doesn't have a base
        loaded_model[0].load_weights(model_file)
        model_base = None
        model_top = loaded_model[0]
    else:
        loaded_model[1].load_weights(model_file)
        model_base = loaded_model[0]
        model_top = loaded_model[1]

    if verbose:
        #print "BASE MODEL"
        #model_base.summary()

        print "TOP MODEL"
        model_top.summary()

    return model_base, model_top, model_settings

def evaluator_test_on_dataset(model_base, model_top, model_settings, dataset):
    [x, y] = dataset.getDataLabels()
    osm = dataset.getDataLabels_only_osm()
    print len_(x), len_(y)

    if model_settings["model_type"] is 'simple_cnn_with_top':
        labels_base = model_base.predict(x, batch_size=32, verbose=1)
        labels_predicted = model_top.predict(labels_base, batch_size=32, verbose=1)
    elif model_settings["model_type"] is 'img_osm_mix':
        labels_base = model_base.predict(x, batch_size=32, verbose=1)
        osm_input = osm
        labels_predicted = model_top.predict([osm_input, labels_base], batch_size=32, verbose=1)
    elif model_settings["model_type"] is 'osm_only':
        osm_input = osm
        labels_predicted = model_top.predict(osm_input, batch_size=32, verbose=1)

    print len_(labels_predicted)
    print labels_predicted

def load_tmp_dataset():
    model_settings = {}
    # HACK
    model_settings["dataset_name"] = "miniset_640px"
    model_settings["pixels"] = 640
    model_settings["number_of_images"] = None
    model_settings["seed"] = 13

    #Settings["models"][0]["dump_file_override"] = 'SegmentsData.dump'
    model_settings["dump_file_override"] = 'SegmentsData_mark100.dump'

    dataset = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                                                       desired_number=model_settings["number_of_images"],
                                                       seed=model_settings["seed"],
                                                       filename_override=model_settings["dump_file_override"])
    # hack over
    return dataset

def evaluator(model_file, settings_file):
    model_base, model_top, model_settings = evaluator_load_model(model_file, settings_file)

    dataset = load_tmp_dataset()

    evaluator_test_on_dataset(model_base, model_top, model_settings, dataset)
