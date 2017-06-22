import os
path_folder = os.path.dirname(os.path.abspath(__file__))

path_folder += '/data/k-fold-tests/5556x_markable_640x640__ExpandDataset_5556x_markable_640x640_kfold10/'

original_history_path = path_folder+'original____1714013.arien-pro.ics.muni.cz_ExpandDataset_5556x_markable_640x640_kfold10_originalComparison/history/5556x_markable_640x640_original_5556x_markable_640x640_500.npy'
extended_history_path = path_folder+'expanded___1714012.arien-pro.ics.muni.cz_ExpandDataset_5556x_markable_640x640_kfold10/history/5556x_markable_640x640_2x_expanded_expanded_5556x_markable_640x640_2x_expanded_500.npy'

from Downloader.VisualizeHistory import loadHistory, visualize_history, visualize_special_histories
from Omnipresent import len_
from ResultsGraphing.custom import visualize_special_histories_custom, count_averages, draw_items_for_legend, onefrom, draw_normal_data, draw_titles_legends, draw_avg_data, save

original_history = loadHistory(original_history_path)
extended_history = loadHistory(extended_history_path)


colors1 = ['grey', 'lightgreen', 'red', 'green'] # << Green is original
colors2 = ['grey', 'lightblue', 'red', 'blue']   # << Blue  is extended
#          train_color, val_color, avg_train_color, avg_val_color

original_history = count_averages(original_history, 'loss')
extended_history = count_averages(extended_history, 'loss')

print original_history.keys()


import matplotlib.pyplot as plt
plt.figure()


items_to_draw  = [original_history["avg_val_loss"], onefrom(original_history,"val_loss")]
items_to_draw += [extended_history["avg_val_loss"], onefrom(extended_history,"val_loss")]

names_to_print  = ["original average val", "original val"]
names_to_print += ["extended average val", "extended val"]
colors_to_use  = [colors1[3], colors1[1], colors2[3], colors2[1]]
linestyles = ['solid', 'dashed', 'solid', 'dashed']

leg = []
[plt, leg] = draw_items_for_legend(plt, leg, items_to_draw, names_to_print, colors_to_use, linestyles)

plt = draw_normal_data("val_loss", original_history["all_histories_of_this_model"], colors1[1], 'dashed', plt)
plt = draw_normal_data("val_loss", extended_history["all_histories_of_this_model"], colors2[1], 'dashed', plt)

plt = draw_avg_data(original_history["avg_val_loss"], colors1[3], 'solid', plt)
plt = draw_avg_data(extended_history["avg_val_loss"], colors2[3], 'solid', plt)

custom_title = 'original vs extended model'
draw_titles_legends(plt, leg, custom_title)

save(plt,True,'graphs/1_original-expand_5556x_markable_640x640/automatic')

plt.show()
plt.clf()





# test this:
'''
# best_validation_errors, best_training_errors
from Downloader.VisualizeHistory import visualize_whiskered_boxed

data_for_whiskeredboxes = [original_history["last_training_errors"], original_history["best_training_errors"],
                           original_history["last_validation_errors"], original_history["best_validation_errors"]]
names = ["last_train", "best_train", "last_val", "best_val"]
title = 'AllErrors'
graph_file = '_kfoldcrossvalidation_AllErrors.png'
visualize_whiskered_boxed(data_for_whiskeredboxes, names=names,
                          show=True, save=False, save_path=graph_file, custom_title=title)
'''