from DatasetObj import Dataset
import random

ABS_PATH_TO_PRJ = '/home/ekmek/Project II/MGR-Project-Code/'

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

#d = load_8376_resized_299x299()
#d.statistics()
#d.plotHistogram()