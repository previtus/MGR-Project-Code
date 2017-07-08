from DatasetObj import Dataset
import os.path
from FileHelperFunc import get_project_folder

ABS_PATH_TO_PRJ = get_project_folder()

def determineUniqueId(dataset_nickname, desired_number,seed):
    '''
    Each dataset needs its own unique name build from the parameters which influence its shape.
    Later we name the feature files with this name and thus it needs to be linked with each dataset.
    :param dataset_nickname: id
    :param desired_number: number of images, can be None if all
    :param seed: seed for random data shuffling
    :return: string of unique id
    '''
    unique_id = dataset_nickname
    if desired_number is not None:
        unique_id = unique_id+'-'+str(desired_number)
    else:
        unique_id = unique_id + '-full'
    if seed is not None:
        unique_id = unique_id+'-seed'+str(seed)
    return unique_id

def prepareDataset(path, dims, desired_number, seed):
    '''
    Create dataset object and prepare it from the suggested Segments file.
    :param path: path
    :param dims: pixel sizes list (width and height)
    :param desired_number: number of images, can be None if all
    :param seed: seed for random data shuffling
    :return: dataset object
    '''
    dataset = Dataset()
    dataset.init_from_segments(path, img_width=dims[0], img_height=dims[1])
    if desired_number is None:
        return dataset

    subset = dataset.spawnUniformSubset(desired_number)
    return subset

def get_path_for_dataset(folder, filename_override):
    '''
    Get path to dataset from couple of default values, or use suggested name
    :param folder: name of the folder, will be joined to the project path
    :param filename_override: suggested name of dataset dump file
    :return: path
    '''
    path_r100 = ABS_PATH_TO_PRJ+'Data/StreetViewData/'+folder+'/SegmentsData_marked_R100.dump'
    path = ABS_PATH_TO_PRJ+'Data/StreetViewData/'+folder+'/SegmentsData.dump'

    path_override = ABS_PATH_TO_PRJ+'Data/StreetViewData/'+folder+'/' + filename_override

    if os.path.isfile(path_r100):
        path = path_r100

    if filename_override <> '' and os.path.isfile(path_override):
        path = path_override
    return path

def load_custom(folder, pixels, desired_number=None, seed=None, filename_override=''):
    '''
    Load dataset from one of prepared folders. Main method to load datasets.
    :param folder: folder name inside StreetViewData
    :param pixels: pixel size
    :param desired_number: number of images, can be None if all
    :param seed: seed for random data shuffling
    :param filename_override: if the name is not SegmentsData_marked_R100.dump or SegmentsData.dump
    :return: dataset object
    '''
    # folder should be name of the dir, like 50x_markable_350x350
    unique_id = determineUniqueId(folder+str(pixels),desired_number,seed)

    path = get_path_for_dataset(folder, filename_override)
    print "#  Loading dataset at", path

    dataset = prepareDataset(path, [pixels, pixels], desired_number, seed)

    dataset.unique_id = unique_id

    print "Loaded dataset with unique_id=", unique_id, ", statistics:"
    dataset.statistics()
    return dataset
