import os

def get_project_folder():
    '''
    Gives us the path to MGR-Project-Code from a list of allowed folders.
    :return:
    '''
    PATH_ALTERNATIVES = ['/home/ekmek/Project II/MGR-Project-Code/', '/storage/brno2/home/previtus/MGR-Project-Code/', '/home/ekmek/Vitek/MGR-Project-Code/']
    ABS_PATH_TO_PRJ = use_path_which_exists(PATH_ALTERNATIVES)
    return ABS_PATH_TO_PRJ

def get_geojson_path():
    '''
    Gives us the path directly to attractivity_previtus_data_1_edges.geojson from a list of allowed paths
    :return:
    '''
    folders = ['/home/ekmek/Desktop/Project II/graph_new_data/',
                   '/home/ekmek/Vitek/graph_new_data/',
                    '/storage/brno2/home/previtus/important_files/']
    folder = use_path_which_exists(folders)

    return folder+'attractivity_previtus_data_1_edges.geojson'

def use_path_which_exists(list_of_possible_paths):
    '''
    From a list of possible paths choose the one which exists.
    :param list_of_possible_paths: possible paths
    :return: working path
    '''
    used_path = ''

    for path in list_of_possible_paths:
        if os.path.exists(path):
            used_path = path

    if used_path == '':
        print "Error, cannot locate the path of project, will likely fail!"

    return used_path

def file_exists(fname):
    ''' Does file exist, returns boolean.'''
    return os.path.isfile(fname)

def get_folder_from_file(fname):
    ''' Get folder name from path to a file.'''
    return os.path.dirname(fname) + '/'

def folder_exists(directory):
    ''' Does folder with this name exist, returns boolean'''
    return os.path.exists(directory)

def make_folder_ifItDoesntExist(directory):
    ''' Make a new directory, if it didn't previously exist.'''
    if not os.path.exists(directory):
        os.makedirs(directory)

import shutil, errno
def copy_folder(src, dst):
    ''' Copy and paste folders. Used for dataset augmentation.'''
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def copy_file(src, dst):
    ''' Copy and paste file.'''
    try:
        shutil.copy(src, dst)
    except OSError as exc:
        raise

import hashlib
def md5(fname):
    ''' Get md5 hash of a file.'''
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
