import os
from Omnipresent import len_
from Downloader.VisualizeHistory import loadHistory
from ResultsGraphing.custom import finally_show, plot_2x2_detailed, count_averages, save_plot, plot_only_averages, boxplots_in_row_custom611, plot_4x4_derailed_boxes, plot_together

dir_folder = os.path.dirname(os.path.abspath(__file__))

###
"""
The idea:
    Compare OSM model on with different settings of width and depth.
    We have grid of 4x4:
        depth = 1,2,3,4
        width = 32,64,128,256
    
    with dataset: 5556x_markable_640x640 i think
    
    Two figures:
        glorious 4x4 grid! with last epoch val
        
        cut into one row or column
        

"""
SAVE = True

path_folder = dir_folder + '/data/k-fold-tests/6.2.3. OSM model GRID 4x4/'
out_folder_1 = dir_folder + '/graphs/6.2.3._OSM_model_GRID_4x4/fig1_4x4madness'
out_folder_2 = dir_folder + '/graphs/6.2.3._OSM_model_GRID_4x4/fig2_cutOfD2fixed'

depths = [1,2,3,4]
#widths = [32,64,128,256]
widths = [256,128,64,32]

data_paths = {}
for d in depths:
    for w in widths:
        ind = 'w' + str(w) + '_d' + str(d)
        name = path_folder + 'w'+str(w)+'_depth'+str(d)+'.npy'
        data_paths[ind] = name


hard_colors = ['red', 'green', 'blue', 'orange']
light_colors = ['pink', 'lightgreen', 'lightblue', 'yellow']

# FIGURE 1

special_histories = {}

for key in data_paths.keys():
    special_histories[key] = loadHistory(data_paths[key])
    special_histories[key] = count_averages(special_histories[key], 'loss')

print special_histories.keys()

import matplotlib.pyplot as plt
plt, figure = plot_4x4_derailed_boxes(plt, special_histories)

save_plot(plt, SAVE, out_folder_1)

# FIGURE 2

# show one line or column
chosen_d = [2]
chosen_w = [256,128,64,32]

selected_histories = []
data_names = []
both_colors = []
both_data_names = []

hard_colors = ['red', 'green', 'blue', 'orange']
light_colors = ['pink', 'lightgreen', 'lightblue', 'yellow']
i = 0

data_paths = {}
for d in chosen_d:
    for w in chosen_w:
        ind = 'w' + str(w) + '_d' + str(d)
        item = special_histories[ind]
        name = 'depth ' + str(d) + ', width ' + str(w)

        selected_histories.append(item)
        data_names.append(name)

        both_colors.append(light_colors[i])
        both_colors.append(hard_colors[i])
        both_data_names.append(name)
        both_data_names.append("validation " + name)
        i+=1


import matplotlib.pyplot as plt
custom_title = 'Validation error averages'
plt = plot_only_averages(plt, selected_histories, data_names, hard_colors, custom_title, save=[SAVE,out_folder_2])

#plt = plot_only_averages(plt, selected_histories, both_data_names, both_colors, custom_title, save=[SAVE,out_folder_2], just='both')

finally_show(plt)