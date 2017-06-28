import ExperimentRunner.SettingsDefaults as SettingsDefaults

import ModelHandler.ModelOI as ModelOI
import ModelHandler.ModelGenerator as ModelGenerator
import ModelHandler.ModelTester as ModelTester
import DatasetHandler as DatasetHandler
from Omnipresent import len_


def evaluator(model_file, settings_file):
    ### LOAD skeleton of model and dataset
    Settings = SettingsDefaults.load_settings_from_file(settings_file, '', verbose=False)
    print Settings

    Settings["models"][0]["test_existence_of_images"] = False
    Settings["models"][0]["evaluation_after_training"] = True

    if Settings["interrupt"]:
        return 365

    # preparation
    datasets = ModelOI.load_dataset(Settings)

    Settings = ModelOI.prepare_folders(Settings, datasets, verbose=True)

    models = ModelGenerator.get_cnn_models(Settings)

    # cooking
    #ModelTester.cook_features(models, datasets, Settings)
    models = ModelGenerator.get_top_models(models, datasets, Settings)

    if Settings["interrupt"]:
        return 365
    if Settings["report_on_models"]:
        ModelGenerator.report_models(models, Settings)

    ModelOI.save_visualizations(models, Settings)
    ### WEIGHTS to model from file

    print len(models)
    print model_file
    loaded_model = models[0]
    dataset = datasets[0]
    loaded_model[1].load_weights(model_file)

    print "BASE MODEL"
    #loaded_model[0].summary()
    print "TOP MODEL"
    #loaded_model[1].summary()

    # New model is made from the cnn and top model
    full_model = ModelGenerator.join_two_models(loaded_model[0], loaded_model[1])

    print "----- JOINED MODEL"
    #print full_model.summary()


    # HACK
    Settings["models"][0]["dataset_name"] = "miniset_640px"
    Settings["models"][0]["dump_file_override"] = 'SegmentsData.dump'
    model_settings = Settings["models"][0]

    dataset = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                                                       desired_number=model_settings["number_of_images"],
                                                       seed=model_settings["seed"],
                                                       filename_override=model_settings["dump_file_override"])
    # hack over

    [x, y] = dataset.getDataLabels()
    print len_(x), len_(y)

    model_settings["epochs"] = 1

    full_model.compile(optimizer=model_settings["optimizer"], loss=model_settings["loss_func"], metrics=model_settings["metrics"])
    history = full_model.fit(x, y, verbose=1, epochs=model_settings["epochs"], batch_size=32)

    print history
