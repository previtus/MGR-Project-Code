'''
This is the main Experiment runner with Models
'''

import ExperimentRunner.SettingsDefaults as SettingsDefaults
import ModelHandler.ModelOI as ModelOI

def run_many_models(settings_file=None):
    Settings = SettingsDefaults.load_settings_from_file(settings_file, verbose=False)

    # preparation
    Settings = ModelOI.prepare_folders(Settings)

    dataset = ModelOI.load_dataset(Settings)
    print Settings["folders"]



run_many_models('setting_example.py')
