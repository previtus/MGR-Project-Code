from DatasetObj import Dataset
import random

def load_subset_8376_valid_images_640x640_120deg_turns_from_all_segments(desired_number, seed=42):
    '''
    :param desired_number: size of generated subset (for example 1000 out of the 8376)
    :param seed: random seed to allow for equal results every time
    :return:
    '''
    path = '../Data/StreetViewData/8376_valid_images_640x640_120deg_turns_from_all_segments/SegmentsData.dump'
    dataset = Dataset()
    dataset.init_from_segments(path, 640, 640)

    if seed is not None:
        random.seed(seed)

    subset = dataset.spawnUniformSubset(desired_number)

    return subset

def load_8376_valid_images_640x640_120deg_turns_from_all_segments():
    path = '../Data/StreetViewData/8376_valid_images_640x640_120deg_turns_from_all_segments/SegmentsData.dump'
    dataset = Dataset()
    dataset.init_from_segments(path, 640, 640)
    return dataset

def load_3342_calid_images_299x299():
    path = '../Data/StreetViewData/3342_calid_images_299x299/SegmentsData.dump'
    dataset = Dataset()
    dataset.init_from_segments(path, 299, 299)
    return dataset