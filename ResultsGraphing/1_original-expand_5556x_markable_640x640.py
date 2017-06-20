import os
path_folder = os.path.dirname(os.path.abspath(__file__))

path_folder += '/data/k-fold-tests/5556x_markable_640x640__ExpandDataset_5556x_markable_640x640_kfold10/'

original_history_path = path_folder+'original____1714013.arien-pro.ics.muni.cz_ExpandDataset_5556x_markable_640x640_kfold10_originalComparison/history/5556x_markable_640x640_original_5556x_markable_640x640_500.npy'
extended_history_path = path_folder+'expanded___1714012.arien-pro.ics.muni.cz_ExpandDataset_5556x_markable_640x640_kfold10/history/5556x_markable_640x640_2x_expanded_expanded_5556x_markable_640x640_2x_expanded_500.npy'

from Downloader.VisualizeHistory import loadHistory, visualize_history, visualize_special_histories,visualize_special_history
from Omnipresent import len_

original_history = loadHistory(original_history_path)
extended_history = loadHistory(extended_history_path)

print original_history.keys()
print extended_history.keys()

Settings = {}
Settings["folders"] = {}
Settings["folders"]["together_graph_filename"] = ''


#visualize_special_history(original_history, Settings, save=False, show=True)

from ResultsGraphing.custom import visualize_special_histories_custom
import matplotlib.pyplot as plt

plt.figure()

colors1 = ['grey', 'lightgreen', 'red', 'green'] # << Green is original
colors2 = ['grey', 'lightblue', 'red', 'blue']   # << Blue  is extended
#train_color, val_color, avg_train_color, avg_val_color

custom_title = 'original model'
visualize_special_histories_custom(plt, colors1, original_history["all_histories_of_this_model"], plotvalues='loss', show=True, save=False, custom_title=custom_title, just_val=True)

custom_title = 'extended model'
visualize_special_histories_custom(plt, colors2, extended_history["all_histories_of_this_model"], plotvalues='loss', show=True, save=False, custom_title=custom_title, just_val=True)

plt.show()
plt.clf()
