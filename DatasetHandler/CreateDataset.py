from DatasetObj import Dataset
from DatasetVizualizators import GenerateAverageImagesFromDictionary
import random
from FileHelperFunc import use_path_which_exists

PATH_ALTERNATIVES = ['/home/ekmek/Project II/MGR-Project-Code/', '/storage/brno2/home/previtus/MGR-Project-Code/']
ABS_PATH_TO_PRJ = use_path_which_exists(PATH_ALTERNATIVES)

def load_8376_valid_images_640x640_120deg_turns_from_all_segments(desired_number=None, seed=None):
    '''
    :param desired_number: size of generated subset (for example 1000 out of the 8376)
    :param seed: random seed to allow for equal results every time
    :return:
    '''
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/8376_valid_images_640x640_120deg_turns_from_all_segments/SegmentsData.dump'
    dataset = Dataset()
    dataset.init_from_segments(path, 640, 640)
    if desired_number is None:
        return dataset

    if seed is not None:
        random.seed(seed)

    subset = dataset.spawnUniformSubset(desired_number)
    return subset

def load_8376_resized_299x299(desired_number=None, seed=None):
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/8376_valid_images_resized_299x299/SegmentsData.dump'
    dataset = Dataset()
    dataset.init_from_segments(path, 299, 299)
    if desired_number is None:
        return dataset
    if seed is not None:
        random.seed(seed)
    subset = dataset.spawnUniformSubset(desired_number)
    return subset

def load_8376_resized_150x150(desired_number=None, seed=None):
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/8376_valid_images_resized_150x150/SegmentsData.dump'
    dataset = Dataset()
    dataset.init_from_segments(path, 150, 150)
    if desired_number is None:
        return dataset
    if seed is not None:
        random.seed(seed)
    subset = dataset.spawnUniformSubset(desired_number)
    return subset

def load_3342_valid_images_299x299(desired_number=None, seed=None):
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/3342_calid_images_299x299/SegmentsData.dump'
    dataset = Dataset()
    dataset.init_from_segments(path, 299, 299)
    if desired_number is None:
        return dataset

    if seed is not None:
        random.seed(seed)

    subset = dataset.spawnUniformSubset(desired_number)
    return subset

#d = load_8376_valid_images_640x640_120deg_turns_from_all_segments()
#dict = d.MapScoreToImages()
#GenerateAverageImagesFromDictionary(dict,save_to_dir=True,output_folder=ABS_PATH_TO_PRJ+'debugVizAvgDatasetEntry/')
#into_bins = 10
#dict2 = d.MapScoreToImages(into_bins=into_bins)
#print len(dict2)
#print len(dict2[0]), '...', len(dict2[9])
#GenerateAverageImagesFromDictionary(dict2,save_to_dir=True,output_folder=ABS_PATH_TO_PRJ+'debugVizAvgDatasetEntry/'+str(into_bins)+'_bins/')

#into_bins = 4
#dict3 = d.MapScoreToImages(into_bins=into_bins)
#GenerateAverageImagesFromDictionary(dict3,save_to_dir=True,output_folder=ABS_PATH_TO_PRJ+'debugVizAvgDatasetEntry/'+str(into_bins)+'_bins/')

#d.statistics()
#d.plotHistogram()

#path = '/home/ekmek/Project II/MGR-Project-Code/debugVizAvgDatasetEntry/__score-img_pairs/'
#d.DumpFilesIntoDirectory_withScores(target_directory=path)

