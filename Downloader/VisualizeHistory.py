import matplotlib.pyplot as plt
import numpy as np

'''
Example calls:
hi = model.fit(...)

saveHistory(hi.history, 'tmp_saved_history.npy')
visualize_history(loadHistory('tmp_saved_history.npy'))

'''

def visualize_history(hi, show=True, save=False, save_path=''):
    # list all data in history
    print(hi.keys())
    # summarize history for loss
    plt.plot(hi['loss'])
    plt.plot(hi['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    if save:
        plt.savefig(save_path+'loss.png')
    if show:
        plt.show()

    return plt

def visualize_histories(histories, names, show=True, save=False, save_path=''):
    '''
    Visualize multiple histories.

    Example usage:
        h1 = loadHistory('history1.npy')
        h2 = loadHistory('history2.npy')
        visualize_histories([h1, h2], ['history1', 'history2'])
    '''
    i = 0
    leg = []
    for hi in histories:
        n = names[i]
        # list all data in history
        print(hi.keys())
        # summarize history for loss
        plt.plot(hi['loss'])
        plt.plot(hi['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        leg.append(n + '_train')
        leg.append(n + '_test')
        i += 1
    plt.legend(leg, loc='upper left')
    if save:
        plt.savefig(save_path+'loss.png')
    if show:
        plt.show()

    return plt

def saveHistory(history_dict, filename):
    to_be_saved = data = {'S': history_dict}
    np.save(open(filename, 'w'), to_be_saved)

def loadHistory(filename):
    loaded = np.load(open(filename))
    return loaded[()]['S']

#visualize_history(loadHistory('1100downloaded_vII/tmp_saved_history.npy'))

#h1 = loadHistory('/home/ekmek/TEMP_SPACE/MGR-Project-Code/Downloader/ModelImplementations/1_SimpleCNN_3conv_2fc/results/history.npy')
#h2 = loadHistory('/home/ekmek/TEMP_SPACE/MGR-Project-Code/Downloader/ModelImplementations/2_VGG16_no_finetuning/(runs)/now2/results/history.npy')
#h3 = loadHistory('/home/ekmek/TEMP_SPACE/MGR-Project-Code/Downloader/ModelImplementations/2_VGG16_no_finetuning/results/history_finetune.npy')
#visualize_histories([h1, h2, h3], ['simple', 'vgg', 'finetune'],save=True)

