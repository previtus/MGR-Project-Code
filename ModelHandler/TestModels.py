import DatasetHandler.CreateDataset as CreateDataset

from DatasetHandler.FileHelperFunc import use_path_which_exists
from ModelHandler.CreateModel.ModelCooking import CookADataset
from ModelHandler.CreateModel.TopModel import TestTopModel
from Downloader.VisualizeHistory import visualize_histories

import datetime
# Test functions to handle models

def main():
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                   '/home/ekmek/Vitek/Logs/',
                     '/storage/brno2/home/previtus/Logs/']
    local_folder = use_path_which_exists(log_folders)

    dataset = CreateDataset.load_1200x_marked_299x299(desired_number=None, seed=42)
    list_of_features = CookADataset(dataset, local_folder=local_folder)
    histories = []
    histories_names = []
    specific_folder_name = ''

    for features in list_of_features:
        [model_name, filename_features_train, filename_features_test] = features

        now = datetime.datetime.now()
        specific_folder_name = str(now.day) + 'th' + '-' + str(now.hour) + '-' + str(now.minute) + '_' + model_name # <day>th-hour-minute_experimentName
        target_folder = local_folder + specific_folder_name + '/'
        filename_history = target_folder + 'history_' + model_name + '.npy'
        img = local_folder + specific_folder_name

        print filename_history
        history = TestTopModel(dataset, model_name, filename_features_train, filename_features_test, filename_history, img)
        histories.append(history)
        histories_names.append(model_name)

    img = local_folder + specific_folder_name + "_all"
    visualize_histories(histories, histories_names, show=False, save=True, save_path=img)

main()
