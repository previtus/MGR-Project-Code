import os
from Omnipresent import len_
from Downloader.VisualizeHistory import loadHistory
from ResultsGraphing.custom import plot_only_averages, finally_show, count_averages, plot_together,save_plot

dir_folder = os.path.dirname(os.path.abspath(__file__))

###
"""
The idea:
    Test various base cnns.
    We have dataset 5556x_mark_res_299x299 with mix model made with variable base cnn:
    vgg16
    vgg19
    resnet50
    xception
    inception v3
    
    One graph to compare only avg valid.
    One graph to compare everything - maybe thats gonna also be legible.

"""
SAVE = True
path_folder = dir_folder + ''
path_folder = '/home/ekmek/Desktop/__ad_thesis/FANCY_STUFFs/0_alt_diffCNNs_try_299set/'
out_folder_1 = dir_folder + '/graphs/6.2.1._different_CNN_299/fig_average_valerr_299'
out_folder_2 = dir_folder + '/graphs/6.2.1._different_CNN_299/fig_allerr_299'



resnet50 = path_folder + "5556x_mark_res_299x299_resnet50_cnn_100.npy"
vgg16 = path_folder + "5556x_mark_res_299x299_vgg16_cnn_100.npy"
vgg19 = path_folder + "5556x_mark_res_299x299_vgg19_cnn_100.npy"
inception_v3 = path_folder + "5556x_mark_res_299x299_inception_v3_cnn_100.npy"
xception = path_folder + "5556x_mark_res_299x299_xception_cnn_100.npy"

data_paths = [resnet50, vgg16, vgg19, xception, inception_v3]
val_data_names = ["resnet50","vgg16","vgg19","xception","inception_v3"]
train_data_names = ["resnet50","vgg16","vgg19","xception","inception_v3"]

hard_colors = ['red', 'green', 'blue', 'orange', 'purple']
light_colors = ['pink', 'lightgreen', 'lightblue', 'yellow', 'hotpink']
both_colors = []
both_data_names = []

special_histories = []
for i in range(0,len(data_paths)):
    special_histories.append(loadHistory(data_paths[i]))
    special_histories[i] = count_averages(special_histories[i], 'loss')

    both_colors.append(light_colors[i])
    both_colors.append(hard_colors[i])
    both_data_names.append(train_data_names[i])
    both_data_names.append(val_data_names[i]+" validation")

import matplotlib.pyplot as plt
#custom_title = 'Validation error averages'
#plt = plot_only_averages(plt, special_histories, val_data_names, hard_colors, custom_title)
#custom_title = 'Training error averages'
#plt = plot_only_averages(plt, special_histories, train_data_names, light_colors, custom_title, just='train')
custom_title = 'Validation and Training error averages, 299px'
plt = plot_only_averages(plt, special_histories, both_data_names, both_colors, custom_title, just='both',
                         save=[SAVE,out_folder_1])

# FIGURE 2

custom_title = 'Base model comparison, 299px'

colors = []
for c in hard_colors:
    colors.append(c)
    colors.append(c)

names_to_print = []
for i in val_data_names:
    names_to_print.append(i + 'average val')
    names_to_print.append(i + 'val')

print colors
print names_to_print

plt = plot_together(special_histories, names_to_print, colors, custom_title)
save_plot(plt, SAVE, out_folder_2)

finally_show(plt)