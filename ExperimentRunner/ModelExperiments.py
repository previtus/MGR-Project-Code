'''
This is the main Experiment runner with Models
'''

import ExperimentRunner.SettingsDefaults as SettingsDefaults
import ModelHandler.ModelOI
import ModelHandler.ModelGenerator
import ModelHandler.ModelTester

def run_many_models(settings_file=None):
    Settings = SettingsDefaults.load_settings_from_file(settings_file, verbose=False)

    # preparation
    Settings = ModelHandler.ModelOI.prepare_folders(Settings)
    dataset = ModelHandler.ModelOI.load_dataset(Settings)
    models = ModelHandler.ModelGenerator.get_cnn_models(Settings)

    # tests
    ModelHandler.ModelTester.cook_features(models, dataset, Settings)

    #models = ModelGenerator.get_top_models(models, Settings)


run_many_models('setting_example.py')
