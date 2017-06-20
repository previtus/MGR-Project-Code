import numpy as np

def visualize_special_histories_custom(plt, colors, histories, plotvalues='loss', show=True, save=False, save_path='', custom_title=None, just_val=False):

    train_color = colors[0]
    val_color = colors[1]

    avg_train_color = colors[2]
    avg_val_color = colors[3]

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

    return plt
