from Downloader.VisualizeHistory import loadHistory, visualize_history, visualize_histories
import math

f1 = '/home/ekmek/Vitek/Logs/selected_ones_from_server_new_datasets_cooking_and_eval/1538008.arien-pro.ics.muni.cz_640_len_20/history/5556x_minlen20_640px_resnet50_5556x_minlen20_640px_500.npy'
#h = loadHistory(f1)


#visualize_history(h, show=True, save=False, save_path='', show_also='mean_absolute_error')
#visualize_history(h, show=True, save=False, save_path='')

f2 = '/home/ekmek/Vitek/Logs/selected_ones_from_server_new_datasets_cooking_and_eval/1538007.arien-pro.ics.muni.cz_640_len30/history/5556x_minlen30_640px_resnet50_5556x_minlen30_640px_500.npy'

f3 = '/home/ekmek/Vitek/Logs/cook0-5556x_markable_640x640/history/5556x_markable_640x640_5556x_markable_640x640_500.npy'

visualize_histories(
    [loadHistory(f1), loadHistory(f2), loadHistory(f3)], ['split-to-min20m_640px', 'split-to-min30m_640px', 'nosplit_640px'], show=True, save=False, save_path='',
    custom_title='Datasets evaluation, splitting of long edges', just_val=True
)

'''
f3 = '/home/ekmek/Documents/19th-12-42_-newWawe-3rdRoundReuse/history_-newWawe-3rdRoundReuse.npy'
f4 = '/home/ekmek/Documents/19th-12-46_-newWawe-4thHopeNoErrDisplay/history_-newWawe-4thHopeNoErrDisplay.npy'
visualize_histories([loadHistory(f1), loadHistory(f2), loadHistory(f3), loadHistory(f4)], ['1', '2', '3', '4'], show=True, save=False, save_path='')


f3 = '/home/ekmek/Documents/runs_from_may_3-5_big_datasets_wo_gen/histories/5th-19-46_resnet50-640/history_resnet50.npy'
f4 = '/home/ekmek/Documents/runs_from_may_3-5_big_datasets_wo_gen/histories/4th-10-51_resnet50-299/history_resnet50.npy'

visualize_histories(
    [loadHistory(f1), loadHistory(f3), loadHistory(f4)], ['full 640 I', 'full 640 III', 'full 299'], show=True, save=False, save_path='',
    custom_title='640 vs 299', just_val=True
)
'''
