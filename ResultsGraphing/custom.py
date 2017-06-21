import numpy as np

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

def save(plt, save, path):
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
