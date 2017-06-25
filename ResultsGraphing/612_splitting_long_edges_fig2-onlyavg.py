import os
from Omnipresent import len_
from Downloader.VisualizeHistory import loadHistory
from ResultsGraphing.custom import plot_only_averages, finally_show, count_averages

dir_folder = os.path.dirname(os.path.abspath(__file__))

###
"""
The idea:
    Demonstrate effectivity of spliting long edges.
    We have datasets:
        original 5556x_markable_640x640
        minlen10 5556x_minlen10_640px
        minlen20 5556x_minlen20_640px
        minlen30 5556x_minlen30_640px
    with both mixed and image model.
    
    Lets start with mixed model. In total we want to produce 3 figures.
    First is showing validation error in the last epoch of these 4 datasets via box plots.
    Alternatively it can show both the validation and training error.
    Four plot boxes next to each other.
     
    Second is showing averages of the validation error only. All four datasets 
    are in the same image - we show only the average in hope that its more clear.
    One shared graph plot.
    
    Third is a information overload kind of graph,
    we want to draw grid of 2x2 with all four datasets, each having a graph plot with
    both training and validation error over the evolution of epochs.

"""

model_txt = "img" # or img

path_folder = dir_folder + '/data/k-fold-tests/6.1.2. splitting long edges - minlen/'
out_folder = dir_folder + '/graphs/6.1.2._splitting_long_edges-minlen/fig2_average_valerr_'+model_txt

if model_txt == "mix":
    original = path_folder + "mix_original_1760999.npy"
    minlen10 = path_folder + "mix_minlen10.npy"
    minlen20 = path_folder + "mix_minlen20.npy"
    minlen30 = path_folder + "mix_minlen30_1761323.npy"
else:
    original = path_folder + "img_original_1769351.npy"
    minlen10 = path_folder + "img_minlen10_1771003.npy"
    minlen20 = path_folder + "img_minlen20.npy"
    minlen30 = path_folder + "img_minlen30_1769353.npy"

data_paths = [original, minlen10, minlen20, minlen30]
val_data_names = [
    "original",
    "minlen10",
    "minlen20",
    "minlen30"]
train_data_names = [
    "original",
    "minlen10",
    "minlen20",
    "minlen30"]
hard_colors = ['red', 'green', 'blue', 'orange']
light_colors = ['pink', 'lightgreen', 'lightblue', 'yellow']
both_colors = []
both_data_names = []

# subset?
n = 4
data_paths = data_paths[0:n]
val_data_names = val_data_names[0:n]
train_data_names = train_data_names[0:n]
hard_colors = hard_colors[0:n]
light_colors = light_colors[0:n]

special_histories = []
for i in range(0,len(data_paths)):
    special_histories.append(loadHistory(data_paths[i]))
    special_histories[i] = count_averages(special_histories[i], 'loss')

    both_colors.append(light_colors[i])
    both_colors.append(hard_colors[i])
    both_data_names.append(train_data_names[i])
    both_data_names.append("validation "+val_data_names[i])

import matplotlib.pyplot as plt
custom_title = 'Validation error averages'
plt = plot_only_averages(plt, special_histories, val_data_names, hard_colors, custom_title,
                         save=[True,out_folder])
custom_title = 'Training error averages'
plt = plot_only_averages(plt, special_histories, train_data_names, light_colors, custom_title, just='train')
custom_title = 'Validation and Training error averages'
plt = plot_only_averages(plt, special_histories, both_data_names, both_colors, custom_title, just='both')

finally_show(plt)