'''
This is the main Experiment runner with Models
'''

import ExperimentRunner.SettingsDefaults as SettingsDefaults
import ModelHandler.ModelOI as ModelOI
import ModelHandler.ModelGenerator as ModelGenerator
import ModelHandler.ModelTester as ModelTester
from Omnipresent import len_

def run_many_models(settings_file=None):
    Settings = SettingsDefaults.load_settings_from_file(settings_file, verbose=False)

    # preparation
    datasets = ModelOI.load_dataset(Settings)

    Settings = ModelOI.prepare_folders(Settings, datasets, verbose=True)
    models = ModelGenerator.get_cnn_models(Settings)

    # cooking
    ModelTester.cook_features(models, datasets, Settings)
    models = ModelGenerator.get_top_models(models, Settings)
    ModelOI.save_visualizations(models, Settings)

    # tests
    histories = ModelTester.test_models(models, datasets, Settings)

    # save results
    ModelOI.save_histories(histories, Settings)
    ModelOI.graph_histories(histories, Settings)

    ModelOI.save_report(Settings)
    ModelOI.save_models(models, Settings)


run_many_models('setting_example.py')
