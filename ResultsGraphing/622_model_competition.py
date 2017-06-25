import os
from Omnipresent import len_
from Downloader.VisualizeHistory import loadHistory
from ResultsGraphing.custom import finally_show, plot_2x2_detailed, count_averages, save_plot, boxplots_in_row, boxplots_in_row_custom611, plot_two_together, plot_together

dir_folder = os.path.dirname(os.path.abspath(__file__))

###
"""
The idea:
    Compare three models on each interesting dataset.
    We have models:
        img
        osm
        mix
    with datasets: 5556x_markable_640x640, 5556x_minlen30_640px, 5556x_minlen30_640px_2x_expanded .
    
    Three figures each:
        all three plotted together
        box plot of train plus val of the last
        ... and of the best epoch

"""
dataset1 = "5556x_markable_640x640"
dataset2 = "5556x_minlen30_640px"
dataset3 = "5556x_minlen30_640px_2x_expanded"

dataset_txt = "expanded30" # markable or minlen30 or expanded30
SAVE = True

path_folder = dir_folder + '/data/k-fold-tests/6.2.2. model competition - img vs osm vs mix/'
out_folder_1 = dir_folder + '/graphs/6.2.2._model_competition-img-vs-osm-vs-mix/fig1_evolution_' + dataset_txt
out_folder_2 = dir_folder + '/graphs/6.2.2._model_competition-img-vs-osm-vs-mix/fig2_last_epoch_' + dataset_txt
out_folder_3 = dir_folder + '/graphs/6.2.2._model_competition-img-vs-osm-vs-mix/fig3_best_epoch_' + dataset_txt

if dataset_txt == "markable":
    osm = path_folder + "5556x_markable_640x640_osm_1761330.npy"
    img = path_folder + "5556x_markable_640x640_img_1769355.npy"
    mix = path_folder + "5556x_markable_640x640_mix_1761329.npy"
elif dataset_txt == "minlen30":
    osm = path_folder + "5556x_minlen30_640px_osm_1761336.npy"
    img = path_folder + "5556x_minlen30_640px_img_1769353.npy"
    mix = path_folder + "5556x_minlen30_640px_mix_1761323.npy"
else:
    osm = path_folder + "5556x_minlen30_640px_2x_expanded_osm_1761327.npy"
    img = path_folder + "5556x_minlen30_640px_2x_expanded_img_1769354.npy"
    mix = path_folder + "5556x_minlen30_640px_2x_expanded_mix_1761326.npy"

data_paths = [osm, img, mix]
data_names = [
    "OSM",
    "Image",
    "Mixed"]
hard_colors = ['red', 'green', 'blue', 'orange']
light_colors = ['pink', 'lightgreen', 'lightblue', 'yellow']

special_histories = []
for i in range(0,len(data_paths)):
    special_histories.append(loadHistory(data_paths[i]))
    special_histories[i] = count_averages(special_histories[i], 'loss')

# FIGURE 1
import matplotlib.pyplot as plt

names_to_print  = ["OSM average val", "OSM val"]
names_to_print += ["Image average val", "Image val"]
names_to_print += ["Mixed average val", "Mixed val"]
custom_title = 'Models comparison'

colors = ["green", "green", "red", "red", "blue", "blue"]

plt = plot_together(special_histories, names_to_print, colors, custom_title)
save_plot(plt, SAVE, out_folder_1)


# FIGURE 2 state in last

custom_title = 'Validation error in last epoch'
plt, figure = boxplots_in_row_custom611(plt, special_histories, data_names, just='both')

figure.suptitle(custom_title) # needs adjustment of the top value
save_plot(plt, SAVE, out_folder_2)


# FIGURE 3 state in their best epoch

custom_title = 'Validation error in best epoch'
plt, figure = boxplots_in_row_custom611(plt, special_histories, data_names, just='both', BestInstead=True)

figure.suptitle(custom_title) # needs adjustment of the top value
save_plot(plt, SAVE, out_folder_3)


finally_show(plt)