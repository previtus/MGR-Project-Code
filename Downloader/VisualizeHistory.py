import matplotlib, os, errno
# IF WE ARE ON SERVER WITH NO DISPLAY, then:
#print matplotlib.get_backend()
if not('DISPLAY' in os.environ):
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

import numpy as np

'''
Example calls:
hi = model.fit(...)

saveHistory(hi.history, 'tmp_saved_history.npy')
visualize_history(loadHistory('tmp_saved_history.npy'))

'''

def visualize_history(hi, show=True, save=False, save_path='', show_also='', custom_title=None):

    # list all data in history
    print(hi.keys())
    # summarize history for loss
    plt.plot(hi['loss'])
    plt.plot(hi['val_loss'])

    if show_also <> '':
        plt.plot(hi[show_also], linestyle='dotted')
        plt.plot(hi['val_'+show_also], linestyle='dotted')

    if custom_title is None:
        plt.title('model loss')
    else:
        plt.title(custom_title)

    plt.ylabel('loss')
    plt.xlabel('epoch')

    if show_also == '':
        plt.legend(['train', 'test'], loc='upper left')
    else:
        plt.legend(['train', 'test', 'train-'+show_also, 'test-'+show_also], loc='upper left')


    if save:
        filename = save_path #+'loss.png'
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        plt.savefig(filename)
        plt.savefig(filename+'.pdf', format='pdf')

        print "Saved image to "+filename
    if show:
        plt.show()

    plt.clf()
    return plt

def visualize_histories(histories, names, plotvalues='loss', show=True, save=False, save_path='', custom_title=None, just_val=False):

    import matplotlib.pyplot as plt

    '''
    Visualize multiple histories.

    Example usage:
        h1 = loadHistory('history1.npy')
        h2 = loadHistory('history2.npy')
        visualize_histories([h1, h2], ['history1', 'history2'])
    '''
    if custom_title is None:
        custom_title = 'model ' + plotvalues
    if just_val:
        custom_title = custom_title + ' (just validation results)'

    i = 0
    leg = []
    for hi in histories:
        n = names[i]
        # list all data in history
        print(hi.keys())
        # summarize history for loss
        if not just_val:
            plt.plot(hi[plotvalues])
        plt.plot(hi['val_'+plotvalues])
        plt.title(custom_title)
        plt.ylabel('loss')
        plt.xlabel('epoch')
        if not just_val:
            leg.append(n + '')
        leg.append(n + '_val')
        i += 1
    #plt.legend(leg, loc='lower left')
    plt.legend(leg, loc='best')
    if save:
        plt.savefig(save_path) #+plotvalues+'.png')
        plt.savefig(save_path+'.pdf', format='pdf')

    if show:
        plt.show()

    plt.clf()
    return plt

def visualize_special_histories(histories, plotvalues='loss', show=True, save=False, save_path='', custom_title=None, just_val=False):
    '''
    We are visualizing results of a k-fold crossvalidation training. In <histories> we have the individual runs of the experiment.

    :param histories:
    :param names:
    :param plotvalues:
    :param show:
    :param save:
    :param save_path:
    :param custom_title:
    :param just_val:
    :return:
    '''

    train_color = 'grey'
    val_color = 'blue'

    avg_train_color = 'red'
    avg_val_color = 'green'

    avg_train = []
    avg_val = []

    # count the averages

    epochs = len(histories[0][plotvalues])
    for epoch in range(0, epochs):
        trains = []
        vals = []
        for hi in histories:
            train = hi[plotvalues][epoch]
            val = hi['val_'+plotvalues][epoch]
            trains.append(train)
            vals.append(val)
        avg_train.append( np.mean(trains) )
        avg_val.append( np.mean(vals) )

    import matplotlib.pyplot as plt
    plt.figure()

    if custom_title is None:
        custom_title = 'model ' + plotvalues
    if just_val:
        custom_title = custom_title + ' (just validation results)'

    i = 0
    leg = []
    if not just_val:
        leg.append('average training')
    leg.append('average validation')

    if not just_val:
        leg.append('training errors')
    leg.append('validation errors')

    # now averages:
    if not just_val:
        plt.plot(avg_train, color=avg_train_color)
    plt.plot(avg_val, color=avg_val_color)

    for hi in histories:
        # list all data in history
        print(hi.keys())
        # summarize history for loss
        if not just_val:
            plt.plot(hi[plotvalues], linestyle='dashed', color=train_color)
        plt.plot(hi['val_'+plotvalues], linestyle='dashed', color=val_color)
        i += 1

    # OK, but we also want these on top...:
    if not just_val:
        plt.plot(avg_train, color=avg_train_color)
    plt.plot(avg_val, color=avg_val_color)


    plt.title(custom_title)
    plt.ylabel('loss')
    plt.xlabel('epoch')


    #plt.legend(leg, loc='lower left')
    plt.legend(leg, loc='best')
    if save:
        plt.savefig(save_path) #+plotvalues+'.png')
        plt.savefig(save_path+'.pdf', format='pdf')

    if show:
        plt.show()

    plt.clf()
    return plt

def visualize_whiskered_boxed(whiskered_boxes_data, names, show=True, save=False, save_path='', custom_title=''):
    '''
    We are visualizing results of a k-fold crossvalidation training.
    In <whiskered_boxes_data> we have data for whiskered box plots.
    '''

    from DatasetHandler.DatasetVizualizators import zoomOutY

    plt.close()

    plt.figure(figsize=(5, 8))
    legend_on = True
    if custom_title == '':
        custom_title = ','.join(names)

    # mark values
    save_path += custom_title + '.png'

    y_max = 1.0
    y_min = 0.0
    #y_max = -100.0
    #y_min = 100.0
    #for i in whiskered_boxes_data:
    #    y_max = max(max(i),y_max)
    #    y_min = min(min(i),y_min)


    axes = plt.axes()
    import matplotlib.ticker as ticker

    axes.yaxis.set_major_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/10.0))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/100.0))

    #meanpointprops = dict(linewidth=0.0)
    meanpointprops = dict(linewidth=1.0)

    boxplot = plt.boxplot(whiskered_boxes_data, notch=False, showmeans=True, meanprops=meanpointprops)

    #plt.xticks(names)

    if (legend_on):
        boxplot['medians'][0].set_label('median')
        boxplot['means'][0].set_label('mean')
        boxplot['fliers'][0].set_label('outlayers')
        # boxplot['boxes'][0].set_label('boxes')
        # boxplot['whiskers'][0].set_label('whiskers')
        boxplot['caps'][0].set_label('caps')

        #axes.set_xlim([0.7, 1.7])

        plt.legend(numpoints = 1)

    axes.set_title(custom_title)
    axes.set_xticklabels(names)

    zoomOutY(axes, [0.0,1.0], 0.1)

    ## save
    if save:
        plt.savefig(save_path) #+plotvalues+'.png')
        plt.savefig(save_path+'.pdf', format='pdf')

    if show:
        plt.show()

    plt.clf()
    return plt

def saveHistory(history_dict, filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

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

