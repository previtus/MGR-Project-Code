import DatasetHandler.CreateDataset as CreateDataset

from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist
from ModelHandler.CreateModel.ModelCooking import CookADataset
from ModelHandler.CreateModel.TopModel import TestTopModel
from Downloader.VisualizeHistory import visualize_histories

import datetime
# Test functions to handle models

def main(set='50x_markable_640x640', PIXELS=640):
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                   '/home/ekmek/Vitek/Logs/',
                     '/storage/brno2/home/previtus/Logs/']
    local_folder = use_path_which_exists(log_folders)
    make_folder_ifItDoesntExist(local_folder+'shared/')

    dataset = CreateDataset.load_custom(set, PIXELS, desired_number=300, seed=42)

    list_of_features = CookADataset(dataset, local_folder=local_folder)
    histories = []
    histories_names = []
    specific_folder_name = 'size5'

    for features in list_of_features:
        [model_name, filename_features_train, filename_features_test] = features

        now = datetime.datetime.now()
        specific_folder_name = str(now.day) + 'th' + '-' + str(now.hour) + '-' + str(now.minute) + '_' + model_name+"-"+str(PIXELS) # <day>th-hour-minute_experimentName
        target_folder = local_folder + specific_folder_name + '/'
        filename_history = target_folder + 'history_' + model_name + '.npy'
        img = local_folder + specific_folder_name+"-"+str(PIXELS)

        print filename_history
        history = TestTopModel(dataset, model_name, filename_features_train, filename_features_test, filename_history, img)
        histories.append(history)
        histories_names.append(model_name)

    img = local_folder + specific_folder_name + "_all_PX"+str(PIXELS)
    visualize_histories(histories, histories_names, show=False, save=True, save_path=img)

main()
main(set='1200x_markable_299x299', PIXELS=299)
