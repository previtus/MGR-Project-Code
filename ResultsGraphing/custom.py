import numpy as np
from Omnipresent import len_

def onefrom(ar, plotvalues):
    return ar["all_histories_of_this_model"][0][plotvalues]

def count_averages(special_history, plotvalues):
    histories = special_history["all_histories_of_this_model"]

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

    special_history['avg_'+plotvalues] = avg_train
    special_history['avg_val_'+plotvalues] = avg_val

    return special_history

def draw_normal_data(plotvalues, items, color, linestyle, plt):
    for item in items:
        plt.plot(item[plotvalues], linestyle=linestyle, color=color)

    return plt

def draw_avg_data(item, color, linestyle, plt):
    plt.plot(item, linestyle=linestyle, color=color)

    return plt

def draw_items_for_legend(plt, leg, items_to_draw, names_to_print, colors_to_use, linestyles):
    for i in range(0, len(items_to_draw)):
        item = items_to_draw[i][0]

        color = colors_to_use[i]
        linestyle = linestyles[i]
        name = names_to_print[i]

        plt.plot(item, linestyle=linestyle, color=color)
        leg.append(name)
    return [plt, leg]

def draw_titles_legends(plt, leg, custom_title):
    plt.title(custom_title)
    plt.ylabel('loss')
    plt.xlabel('epoch')

    #plt.legend(leg, loc='lower left')
    plt.legend(leg, loc='best')

    return plt

def save_plot(plt, save, path):
    from DatasetHandler.FileHelperFunc import get_folder_from_file, make_folder_ifItDoesntExist
    dir = get_folder_from_file(path)
    make_folder_ifItDoesntExist(dir)

    if save:
        plt.savefig(path)
        plt.savefig(path+'.pdf', format='pdf')

    return plt

def visualize_special_histories_custom(plt, leg, colors, special_history, plotvalues='loss', show=True, save=False, save_path='', custom_title=None, just_val=False):
    histories = special_history["all_histories_of_this_model"]
    avg_train = special_history['avg_'+plotvalues]
    avg_val = special_history['avg_val_'+plotvalues]

    train_color = colors[0]
    val_color = colors[1]
    avg_train_color = colors[2]
    avg_val_color = colors[3]



    i = 0


    # now averages:
    if not just_val:
        plt.plot(avg_train, linestyle='solid', color=avg_train_color)
    plt.plot(avg_val, linestyle='solid', color=avg_val_color)

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


    if save:
        plt.savefig(save_path) #+plotvalues+'.png')
        plt.savefig(save_path+'.pdf', format='pdf')

    return plt

def finally_show(plt):
    # will show all drawn graphs at once
    plt.show()

def plot_only_averages(plt, special_histories, data_names, colors, custom_title, just='val', save=[False,'']):
    items_to_draw = []
    names_to_print = []
    linestyles = []

    for i in range(0,len(special_histories)):
        special_histories[i] = count_averages(special_histories[i], 'loss')
        if just=='val':
            items_to_draw.append(special_histories[i]['avg_val_loss'])
            linestyles.append('solid')
            names_to_print.append(data_names[i])

        if just == 'train':
            items_to_draw.append(special_histories[i]['avg_loss'])
            linestyles.append('solid')
            names_to_print.append(data_names[i])

        if just == 'both':
            items_to_draw.append(special_histories[i]['avg_loss'])
            linestyles.append('dashed')
            items_to_draw.append(special_histories[i]['avg_val_loss'])
            linestyles.append('solid')

            names_to_print.append(data_names[2*i])
            names_to_print.append(data_names[2*i+1])

    print len_(items_to_draw), items_to_draw
    print len_(names_to_print), names_to_print
    print special_histories[0].keys()

    plt.figure()

    leg = []
    [plt, leg] = draw_items_for_legend(plt, leg, items_to_draw, names_to_print, colors, linestyles)

    for i in range(0,len(items_to_draw)):
        avg = items_to_draw[i]
        plt = draw_avg_data(avg, colors[i], linestyles[i], plt)

    draw_titles_legends(plt, leg, custom_title)

    save_plot(plt, save[0], save[1])

    plt.draw()
    return plt