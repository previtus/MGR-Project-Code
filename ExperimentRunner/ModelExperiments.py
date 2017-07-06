'''
This is the main Experiment runner with Models
'''

import ExperimentRunner.SettingsDefaults as SettingsDefaults
import ModelHandler.ModelOI as ModelOI
import ModelHandler.ModelGenerator as ModelGenerator
import ModelHandler.ModelTester as ModelTester
from Omnipresent import len_

def experiment_runner(settings_file=None, job_id=''):
    '''
    Main experiment runner function, controls the run of the whole testing scheme.
    :param settings_file: specification of path to Settings file
    :param job_id: unque id, given by the scheduling program
    :return:
    '''

    # Load settings
    Settings = SettingsDefaults.load_settings_from_file(settings_file, job_id, verbose=False)
    if Settings["interrupt"]:
        return 365

    # Preparation of dataset and models
    datasets = ModelOI.load_dataset(Settings)

    Settings = ModelOI.prepare_folders(Settings, datasets, verbose=True)

    models = ModelGenerator.get_cnn_models(Settings)

    # cooking of reusable features
    ModelTester.cook_features(models, datasets, Settings)
    # build the rest of the model (now with information about feature files available)
    models = ModelGenerator.get_top_models(models, datasets, Settings)
    if Settings["interrupt"]:
        return 365
    if Settings["report_on_models"]:
        ModelGenerator.report_models(models, Settings)

    ModelOI.save_visualizations(models, Settings)

    # training
    histories = ModelTester.train_models(models, datasets, Settings)

    # save results
    ModelOI.save_histories(histories, Settings)
    ModelOI.graph_histories(histories, Settings)

    ModelOI.save_report(Settings)
    ModelOI.save_models(models, Settings)

    ModelOI.send_mail_with_graph(Settings)
    ModelOI.save_metacentrum_report(Settings)
