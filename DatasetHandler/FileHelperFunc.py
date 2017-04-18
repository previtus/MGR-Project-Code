import os

def use_path_which_exists(list_of_possible_paths):
    used_path = ''

    for path in list_of_possible_paths:
        if os.path.exists(path):
            used_path = path

    if used_path == '':
        print "Error, cannot locate the path of project, will likely fail!"

    return used_path
