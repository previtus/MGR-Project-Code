import os

def get_project_folder():
    '''
    Gives us the path to MGR-Project-Code
    :return:
    '''
    PATH_ALTERNATIVES = ['/home/ekmek/Project II/MGR-Project-Code/', '/storage/brno2/home/previtus/MGR-Project-Code/', '/home/ekmek/Vitek/MGR-Project-Code/']
    ABS_PATH_TO_PRJ = use_path_which_exists(PATH_ALTERNATIVES)
    return ABS_PATH_TO_PRJ

def get_geojson_path():
    '''
    Gives us the path directly to attractivity_previtus_data_1_edges.geojson
    :return:
    '''
    folders = ['/home/ekmek/Desktop/Project II/graph_new_data/',
                   '/home/ekmek/Vitek/graph_new_data/',
                    '/storage/brno2/home/previtus/important_files/']
    folder = use_path_which_exists(folders)

    return folder+'attractivity_previtus_data_1_edges.geojson'

def use_path_which_exists(list_of_possible_paths):
    used_path = ''

    for path in list_of_possible_paths:
        if os.path.exists(path):
            used_path = path

    if used_path == '':
        print "Error, cannot locate the path of project, will likely fail!"

    return used_path

def make_folder_ifItDoesntExist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
