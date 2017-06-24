import os
from Omnipresent import len_
from Downloader.VisualizeHistory import loadHistory
from ResultsGraphing.custom import finally_show, plot_4x4_detailed, count_averages, save_plot, boxplots_in_row, boxplots_in_row_custom611, plot_two_together, plot_together

dir_folder = os.path.dirname(os.path.abspath(__file__))

###
"""
The idea:
    Compare augmented datasets.
    original
    expanded
    aggresively expanded

"""
dataset1 = "5556x_markable_640x640"
dataset2 = "5556x_minlen30_640px"

dataset_txt = "minlen30" # markable or minlen30

path_folder = dir_folder + '/data/k-fold-tests/6.1.3. augmentation - original, expanded, agg expanded/'
out_folder_1 = dir_folder + '/graphs/6.1.3. augmentation - original, expanded, agg expanded/figLeft_'
out_folder_2 = dir_folder + '/graphs/6.1.3. augmentation - original, expanded, agg expanded/figRight_'

if dataset_txt == "markable":
    original = path_folder + "mix_5556x_markable_640x640_original_1760999.npy"
    expanded = path_folder + "mix_5556x_markable_640x640_expanded_1760987.npy"
    aggresive = path_folder + ".npy"
else:
    original = path_folder + "mix_5556x_minlen30_640px_original_1713895.npy"
    expanded = path_folder + "mix_5556x_minlen30_640px_expanded_1714014.npy"
    aggresive = path_folder + ".npy"

data_paths = [original, expanded, expanded]
data_names = [
    "original",
    "expanded",
    "willbeexpanded"]
hard_colors = ['red', 'green', 'blue', 'orange']
light_colors = ['pink', 'lightgreen', 'lightblue', 'yellow']

special_histories = []
for i in range(0,len(data_paths)):
    special_histories.append(loadHistory(data_paths[i]))
    special_histories[i] = count_averages(special_histories[i], 'loss')

custom_title = 'Validation error in last epoch'

import matplotlib.pyplot as plt
plt, figure = boxplots_in_row_custom611(plt, special_histories, data_names, just='both')

figure.suptitle(custom_title) # needs adjustment of the top value
save_plot(plt, True, out_folder_1)


names_to_print  = ["original average val", "original val"]
names_to_print += ["expanded average val", "expanded val"]
names_to_print += ["willbemore average val", "willbemore val"]
custom_title = 'Dataset Augmentation'

colors = ["green", "green", "red", "red", "blue", "blue"]

plt = plot_together(special_histories, names_to_print, colors, custom_title)
save_plot(plt, True, out_folder_2)

finally_show(plt)