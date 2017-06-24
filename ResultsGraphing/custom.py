import numpy as np
import math
from Omnipresent import len_
from DatasetHandler.DatasetVizualizators import zoomOutY
import matplotlib.ticker as ticker


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

def draw_normal_data(plotvalues, items, color, linestyle, plt, alpha_def=0.2):
    lines = []
    for item in items:
        line = plt.plot(item[plotvalues], linestyle=linestyle, color=color, alpha=alpha_def)
        lines.append(line)

    return plt, lines

def draw_avg_data(item, color, linestyle, plt):
    line = plt.plot(item, linestyle=linestyle, color=color)

    return plt, line

def draw_items_for_legend(plt, leg, items_to_draw, names_to_print, colors_to_use, linestyles, alphas=None):
    for i in range(0, len(items_to_draw)):
        item = items_to_draw[i][0]

        color = colors_to_use[i]
        linestyle = linestyles[i]
        name = names_to_print[i]

        if alphas is None:
            alpha = 1.0
        else:
            alpha = alphas[i]

        plt.plot(item, linestyle=linestyle, color=color, alpha=alpha)
        leg.append(name)
    return [plt, leg]

def draw_titles_legends(plt, leg, custom_title):
    plt.title(custom_title)
    plt.ylabel('loss')
    plt.xlabel('epoch')

    #plt.legend(leg, loc='lower left')
    plt.legend(leg, loc='best')

    return plt

def save_plot(plt, save, path, dpi=200):
    from DatasetHandler.FileHelperFunc import get_folder_from_file, make_folder_ifItDoesntExist
    dir = get_folder_from_file(path)
    make_folder_ifItDoesntExist(dir)

    if save:
        plt.savefig(path, dpi=dpi)
        plt.savefig(path+'.pdf', format='pdf', dpi=dpi)

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
        plt, _ = draw_avg_data(avg, colors[i], linestyles[i], plt)

    draw_titles_legends(plt, leg, custom_title)

    save_plot(plt, save[0], save[1])

    plt.draw()
    return plt

def plot_one_one_subplot(axarritem, data, title):
    #axarritem.plot(data['avg_val_loss'])
    axarritem.set_title(title)

    items_to_draw = [data["avg_val_loss"], onefrom(data, "val_loss")]

    names_to_print = ["original average val", "original val", "original average train", "original train"]
    colors_to_use = ['red', 'grey']
    linestyles = ['solid', 'dashed']

    leg = []
    alphas = [1.0, 0.2, 1.0, 0.2]
    [axarritem, leg] = draw_items_for_legend(axarritem, leg, items_to_draw, names_to_print, colors_to_use, linestyles, alphas)

    axarritem, lines_train = draw_normal_data("loss", data["all_histories_of_this_model"], colors_to_use[1], 'dashed', axarritem)
    axarritem, line_train_avg = draw_avg_data(data["avg_loss"], colors_to_use[1], 'solid', axarritem)

    axarritem, lines_val = draw_normal_data("val_loss", data["all_histories_of_this_model"], colors_to_use[0], 'dashed', axarritem)
    axarritem, line_val_avg = draw_avg_data(data["avg_val_loss"], colors_to_use[0], 'solid', axarritem)

    return line_val_avg + lines_val[0] + line_train_avg + lines_train[0]

def plot_4x4_detailed(plt, special_histories, data_names):
    figure, axarr = plt.subplots(2, 2, sharex=True, sharey=True)

    plot_one_one_subplot(axarr[0, 0], special_histories[0], data_names[0])
    plot_one_one_subplot(axarr[0, 1], special_histories[1], data_names[1])
    plot_one_one_subplot(axarr[1, 0], special_histories[2], data_names[2])
    lines = plot_one_one_subplot(axarr[1, 1], special_histories[3], data_names[3])

    '''
    axarr[0, 1].scatter(x, y)
    axarr[0, 1].set_title('Axis [0,1]')
    axarr[1, 0].plot(x, y ** 2)
    axarr[1, 0].set_title('Axis [1,0]')
    axarr[1, 1].scatter(x, y ** 2)
    axarr[1, 1].set_title('Axis [1,1]')
    '''
    # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
    figure.subplots_adjust(hspace=0.24, wspace=0.1, bottom=0.19, top=0.92, left=0.1, right=0.95)

    # 1053x677 pixels
    #f.subplots_adjust(hspace=0.2, wspace=0.1, bottom=0.2, top=0.9, left=0.1, right=0.95)

    plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
    plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)

    # Big frame around
    ax = figure.add_subplot(111, frameon=False)

    #print lines
    labels = ["val avg","val", "train avg", "train"]

    plt.figlegend(lines, labels, loc='lower center', ncol=4, labelspacing=0., bbox_to_anchor=(0.5, 0.))
    #f.legend(lines, labels, loc=(0.5, 0), ncol=5)

    plt.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    plt.xlabel("epoch")
    plt.ylabel("loss")

    return plt, figure

def boxplots_in_row_NVM(plt, special_histories, data_names):
    data_for_whiskeredboxes = []
    names = []
    for i in range(0,len(special_histories)):
        data_for_whiskeredboxes += special_histories[i]["last_validation_errors"], special_histories[i]["last_training_errors"]
        name = data_names[i]
        names += [name+" val", name+" train"]

    y_max = 1.0
    y_min = 0.0

    y_max = -100.0
    y_min = 100.0
    for i in data_for_whiskeredboxes:
        y_max = max(max(i),y_max)
        y_min = min(min(i),y_min)
    y_min = 0.0
    print y_min, y_max
    y_max = math.ceil( y_max * 100 ) * 0.01

    axes = plt.axes()
    axes.yaxis.set_major_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/10.0))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/100.0))

    boxplot = plt.boxplot(data_for_whiskeredboxes, notch=False, showmeans=True)

    zoomOutY(axes, [y_min,y_max], 0.1)

    axes.set_xticklabels(names)

    legend_on = True

    if (legend_on):
        boxplot['medians'][0].set_label('median')
        boxplot['means'][0].set_label('mean')
        boxplot['fliers'][0].set_label('outlayers')
        # boxplot['boxes'][0].set_label('boxes')
        # boxplot['whiskers'][0].set_label('whiskers')
        boxplot['caps'][0].set_label('caps')

        #axes.set_xlim([0.7, 2.7])
        plt.legend(numpoints = 1)

    return plt

def figure_out_y(special_histories):
    data = []
    y_max = -100.0
    y_min = 100.0

    for i in range(0,len(special_histories)):
        a = special_histories[i]["last_validation_errors"]
        b = special_histories[i]["last_training_errors"]

        y_max = max(max(a),y_max)
        y_min = min(min(a),y_min)
        y_max = max(max(b),y_max)
        y_min = min(min(b),y_min)

    y_min = 0.0
    y_max = math.ceil( y_max * 100 ) * 0.01
    print y_min, y_max
    return y_min, y_max

def one_boxplot(axarritem, data, title, legend_on=False):
    valdata = data["last_validation_errors"]
    traindata = data["last_training_errors"]

    boxplot = axarritem.boxplot([valdata, traindata], labels=['val', 'train'], widths = 0.6, showmeans=True, meanline=True)
    axarritem.set_title(title)


    if (legend_on):
        boxplot['medians'][0].set_label('median')
        boxplot['means'][0].set_label('mean')
        boxplot['fliers'][0].set_label('outlayers')
        # boxplot['boxes'][0].set_label('boxes')
        # boxplot['whiskers'][0].set_label('whiskers')
        boxplot['caps'][0].set_label('caps')

        #axes.set_xlim([0.7, 2.7])
    return boxplot

def boxplots_in_row(plt, special_histories, data_names):
    y_min, y_max = figure_out_y(special_histories)

    figure, axarr = plt.subplots(1, 4, sharex=True, sharey=True) #, figsize=(6, 8)

    one_boxplot(axarr[0], special_histories[0], data_names[0])
    one_boxplot(axarr[1], special_histories[1], data_names[1])
    one_boxplot(axarr[2], special_histories[2], data_names[2])
    one_boxplot(axarr[3], special_histories[3], data_names[3], legend_on=True)

    figure.subplots_adjust(wspace=0, right=0.81, left=0.1)

    plt.legend(numpoints=1, bbox_to_anchor=(1.1, 0.95))

    axarr[0].yaxis.set_major_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/10.0))
    axarr[0].yaxis.set_minor_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/100.0))


    return plt, figure