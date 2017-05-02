from DatasetObj import Dataset
from DatasetVizualizators import GenerateAverageImagesFromDictionary
import random
from FileHelperFunc import get_project_folder

ABS_PATH_TO_PRJ = get_project_folder()

def determineUniqueId(dataset_nickname, desired_number,seed):
    unique_id = dataset_nickname
    if desired_number is not None:
        unique_id = unique_id+'-'+str(desired_number)
    else:
        unique_id = unique_id + '-full'
    if seed is not None:
        unique_id = unique_id+'-seed'+str(seed)
    return unique_id

def prepareDataset(path, dims, desired_number, seed):
    dataset = Dataset()
    dataset.init_from_segments(path, dims[0], dims[1])
    if desired_number is None:
        return dataset

    if seed is not None:
        random.seed(seed)

    subset = dataset.spawnUniformSubset(desired_number)
    return subset

def load_8376_valid_images_640x640_120deg_turns_from_all_segments(desired_number=None, seed=None):
    '''
    :param desired_number: size of generated subset (for example 1000 out of the 8376)
    :param seed: random seed to allow for equal results every time
    :return: subset and a unique identifier, which defines which images we have

    unique identifier depends on the exact folder used as source, the number which we chose by desired_number and seed
    '''

    unique_id = determineUniqueId('data640',desired_number,seed)
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/8376_valid_images_640x640_120deg_turns_from_all_segments/SegmentsData.dump'
    dataset = prepareDataset(path, [640, 640], desired_number, seed)

    dataset.unique_id = unique_id
    return dataset

def load_8376_resized_299x299(desired_number=None, seed=None):
    unique_id = determineUniqueId('data299',desired_number,seed)
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/8376_valid_images_resized_299x299/SegmentsData.dump'
    dataset = prepareDataset(path, [299, 299], desired_number, seed)

    dataset.unique_id = unique_id
    return dataset

def load_8376_resized_150x150(desired_number=None, seed=None):
    unique_id = determineUniqueId('data150',desired_number,seed)
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/8376_valid_images_resized_150x150/SegmentsData.dump'
    dataset = prepareDataset(path, [150, 150], desired_number, seed)

    dataset.unique_id = unique_id
    return dataset

def load_3342_valid_images_299x299(desired_number=None, seed=None):
    unique_id = determineUniqueId('data299subset',desired_number,seed)
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/3342_calid_images_299x299/SegmentsData.dump'
    dataset = prepareDataset(path, [299, 299], desired_number, seed)

    dataset.unique_id = unique_id
    return dataset

def load_1200x_marked_299x299(desired_number=None, seed=None):
    unique_id = determineUniqueId('data299mark',desired_number,seed)
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/1200x_markable_299x299/SegmentsData_marked_R100.dump'
    dataset = prepareDataset(path, [299, 299], desired_number, seed)

    dataset.unique_id = unique_id
    return dataset

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

