import os
from Omnipresent import len_
from Downloader.VisualizeHistory import loadHistory
from ResultsGraphing.custom import finally_show, plot_2x2_detailed, count_averages, save_plot, boxplots_in_row, boxplots_in_row_custom611, plot_two_together, plot_together

dir_folder = os.path.dirname(os.path.abspath(__file__))

###
"""
The idea:
    Compare dataset with 299x299 pixels versus 640x640 pixels.
    We have datasets:
        299   5556x_mark_res_299x299
        640   5556x_markable_640x640
    with both mixed and image model.
    
    Only one plot, but a complicated one.
    On left side we compare validation error of last in box plot.
    On right side we show evolution over epochs of the two datasets in one graph plot.
    
    Its possible to generate these to separately and then join them in tex btw.
"""

SAVE = True
path_folder = dir_folder + '/data/k-fold-tests/6.1.1. pixel size/'
out_folder_3 = dir_folder + '/graphs/6.1.1._pixel_size/fig_Four'

m299_mix = path_folder + "299_mixed_v1.npy"
m640_mix = path_folder + "640_mixed_1760999.npy"

m299_img = path_folder + "299_image_v1.npy"
m640_img = path_folder + "640_image_1769351.npy"

data_paths = [m299_img, m640_img, m299_mix, m640_mix]
data_names = ["image\n299x299", "image\n640x640", "mixed\n299x299", "mixed\n640x640"]
hard_colors = ['red', 'green', 'blue', 'orange']
light_colors = ['pink', 'lightgreen', 'lightblue', 'yellow']

special_histories = []
for i in range(0,len(data_paths)):
    special_histories.append(loadHistory(data_paths[i]))
    special_histories[i] = count_averages(special_histories[i], 'loss')

custom_title = 'Best validation error over epochs'

import matplotlib.pyplot as plt
plt, figure = boxplots_in_row_custom611(plt, special_histories, data_names, BestInstead=True, just='val', show_legend=True, custom_size=(6,6))

figure.suptitle(custom_title) # needs adjustment of the top value
save_plot(plt, True, out_folder_3)

finally_show(plt)