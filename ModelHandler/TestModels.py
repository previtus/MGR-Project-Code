import DatasetHandler.CreateDataset as CreateDataset

from keras.utils import plot_model
from DatasetHandler.FileHelperFunc import use_path_which_exists
from ModelHandler.CreateModel.ModelCooking import CookADataset

# Test functions to handle models

def main():
    log_folders = ['/home/ekmek/Desktop/Project II/MGR-Project-Code/Logs/',
                   '/home/ekmek/Vitek/Logs/',
                     '/storage/brno2/home/previtus/Logs/']
    local_folder = use_path_which_exists(log_folders)
    name_of_the_experiment = 'modelBuilding'

    dataset = CreateDataset.load_1200x_marked_299x299(desired_number=50, seed=42)
    list_of_features = CookADataset(dataset, local_folder=local_folder, name_of_the_experiment=name_of_the_experiment)

    for features in list_of_features:
        print features[0]

main()
