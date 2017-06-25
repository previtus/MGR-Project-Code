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
model_txt = "img" # or img

path_folder = dir_folder + '/data/k-fold-tests/6.1.1. pixel size/'
out_folder_1 = dir_folder + '/graphs/6.1.1._pixel_size/figLeft_boxplotcomp_val_' + model_txt
out_folder_2 = dir_folder + '/graphs/6.1.1._pixel_size/figRight_graphcomp_evol_' + model_txt

# ALTERNATIVES
img_299_2 = '/home/ekmek/Documents/20-6-downs/06-22-recorded/_6.1.1. pixel size/1771008.arien-pro.ics.muni.cz_set4b_pixelSize_img_299_d7/history/5556x_mark_res_299x299_img_with_299_500.npy'
mix_299_2 = '/home/ekmek/Documents/20-6-downs/06-22-recorded/_6.1.1. pixel size/1771009.arien-pro.ics.muni.cz_set4b_pixelSize_mix_299_d7/history/299_mixed_v2.npy'
img_640_2 = '/home/ekmek/Vitek/Mgr project/MGR-Project-Code/ResultsGraphing/data/k-fold-tests/ModelsVersus__tests_of_individual_models/img 5556x_markable_640x640/1769355.arien-pro.ics.muni.cz_TypesOfModels_monoTest_IMG_kfold_d1/history/5556x_markable_640x640_imagemodel_500.npy'

if model_txt == "mix":
    m299 = path_folder + "299_mixed_v1.npy"
    m640 = path_folder + "640_mixed_1760999.npy"

    #m299 = mix_299_2
    # actually mix_299_2 and m299 behave almost the same - stick with m299

else:
    m299 = path_folder + "299_image_v1.npy"
    m640 = path_folder + "640_image_1769351.npy"

    #m299 = img_299_2
    # again behaves very similarly - which is good actually

    #m640 = img_640_2
    # again behavior is stable in both

data_paths = [m299, m640]
data_names = [
    "299x299",
    "640x640"]
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

#finally_show(plt)

names_to_print  = ["299x299 average val", "299x299 val"]
names_to_print += ["640x640 average val", "640x640 val"]
custom_title = 'Pixel size comparison'

colors = ["green", "green", "red", "red"]

plt = plot_together(special_histories, names_to_print, colors, custom_title)
save_plot(plt, SAVE, out_folder_2)

finally_show(plt)