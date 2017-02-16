import matplotlib.pyplot as plt
import numpy as np

'''
Example calls:
hi = model.fit(...)

saveHistory(hi.history, 'tmp_saved_history.npy')
visualize_history(loadHistory('tmp_saved_history.npy'))

'''

def visualize_history(hi):
    # list all data in history
    print(hi.keys())
    # summarize history for accuracy
    plt.plot(hi['acc'])
    plt.plot(hi['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(hi['loss'])
    plt.plot(hi['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

def saveHistory(history_dict, filename):
    to_be_saved = data = {'S': history_dict}
    np.save(open(filename, 'w'), to_be_saved)

def loadHistory(filename):
    loaded = np.load(open(filename))
    return loaded[()]['S']

