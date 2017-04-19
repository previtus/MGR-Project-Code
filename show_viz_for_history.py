from Downloader.VisualizeHistory import loadHistory, visualize_history, visualize_histories
import math

f1 = '/home/ekmek/Documents/19th-12-24_-newWawe-1stRoundShouldCountBoth/history_-newWawe-1stRoundShouldCountBoth.npy'
h = loadHistory(f1)


#visualize_history(h, show=True, save=False, save_path='', show_also='mean_absolute_error')
visualize_history(h, show=True, save=False, save_path='')

'''
f2 = '/home/ekmek/Documents/19th-12-33_-newWawe-2ndRoundReuse/history_-newWawe-2ndRoundReuse.npy'
f3 = '/home/ekmek/Documents/19th-12-42_-newWawe-3rdRoundReuse/history_-newWawe-3rdRoundReuse.npy'
f4 = '/home/ekmek/Documents/19th-12-46_-newWawe-4thHopeNoErrDisplay/history_-newWawe-4thHopeNoErrDisplay.npy'
visualize_histories([loadHistory(f1), loadHistory(f2), loadHistory(f3), loadHistory(f4)], ['1', '2', '3', '4'], show=True, save=False, save_path='')
'''