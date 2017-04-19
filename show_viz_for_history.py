from Downloader.VisualizeHistory import loadHistory, visualize_history
import math

filename_history = '/home/ekmek/Documents/history_VGG16manual-first_experiments.npy'

h = loadHistory(filename_history)

#visualize_history(h, show=True, save=False, save_path='', show_also='mean_absolute_error')
visualize_history(h, show=True, save=False, save_path='')
