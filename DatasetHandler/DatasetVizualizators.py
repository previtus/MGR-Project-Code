import numpy as np
from PIL import Image
import matplotlib, os

#print "importing visual module"

if not('DISPLAY' in os.environ):
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

import matplotlib.ticker as ticker
import matplotlib.backends.backend_pdf
import copy

# customization: http://matplotlib.org/users/customizing.html

def saveAllPlotsToPDF():
    # Save all created plots into a pdf file.
    pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
    for i in plt.get_fignums():
        fig = plt.figure(i)
        pdf.savefig(fig)
    pdf.close()

def xkcd():
    # special style
    plt.xkcd()

def show():
    # show plots on screen
    plt.show()

def GenerateAverageImagesFromDictionary(dict, save_to_dir=None, output_folder=None):
    '''
    Gets a dictionary of d[score_label_value] pointing to an array of images
    :param dict:
    :return: Up to 100 averaged images
    '''
    dict_of_images = {}

    for i in range(0,len(dict)):
        imlist = dict[i]
        N = len(imlist)
        if N > 0:
            w, h = Image.open(imlist[0]).size
            arr = np.zeros((h, w, 3), np.float)
            for im in imlist:
                imarr = np.array(Image.open(im), dtype=np.float)
                arr = arr + imarr / N
            arr = np.array(np.round(arr), dtype=np.uint8)
            dict_of_images[i] = arr

            if save_to_dir is not None:
                out=Image.fromarray(arr,mode="RGB")
                out.save(output_folder+str(i).zfill(3)+"_avgFrom_"+str(N)+".png")
                #out.show()

    return dict_of_images

def plotX_sortValues(dont_touch_this_x, title='', x_min=0.0, x_max=1.0, notReverse=False, custom_x_label = '# of images', custom_y_label = 'Score value'):
    # Visualization of dataset by the method of sorting array by value and plotting.
    x = copy.copy(dont_touch_this_x)
    if notReverse:
        x.sort()
    else:
        x.sort(reverse=True)

    plt.figure()
    axes = plt.axes()
    axes.set_xlabel(custom_x_label)
    axes.set_ylabel(custom_y_label)

    plt.plot(x, color='red')
    axes.fill_between(range(len(x)), x, facecolor='orange', edgecolor='red', alpha=1)

    zoomOut(axes, [0.0, len(x)-1], [x_min, x_max], factor=0.05)

    axes.fill_between(x, 0)

    axes.set_title(title)

def plotHistogram(x, title='', num_bins=100, x_min=0.0, x_max=1.0, custom_x_label = 'Score value', custom_y_label = 'Count of occurances'):
    # Plot histogram from the x data.
    plt.figure()
    axes = plt.axes()

    hist, bins = np.histogram(x, bins=num_bins)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width, color='orange', edgecolor='red')

    axes.xaxis.set_major_locator(ticker.MultipleLocator(np.abs(x_max-x_min)/10.0))
    axes.xaxis.set_minor_locator(ticker.MultipleLocator(np.abs(x_max-x_min)/100.0))

    # add a 'best fit' line
    axes.set_xlabel(custom_x_label)
    axes.set_ylabel(custom_y_label)

    zoomOutY(axes, factor=0.05, only_up=True)
    zoomOutX(axes, [x_min, x_max], factor=0.05)

    # Tweak spacing to prevent clipping of ylabel

    axes.set_title(title)

def plotWhisker(data, title='', y_min=0.0, y_max=1.0, legend_on=True, notch=True):
    # Plot box plot / whisker graph from data.
    plt.figure(figsize=(5, 8))
    axes = plt.axes()
    axes.yaxis.set_major_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/10.0))
    axes.yaxis.set_minor_locator(ticker.MultipleLocator(np.abs(y_max-y_min)/100.0))

    meanpointprops = dict(linewidth=1.0)
    boxplot = plt.boxplot(data, notch=notch, showmeans=True, meanprops=meanpointprops)

    plt.xticks([])

    if (legend_on):
        boxplot['medians'][0].set_label('median')
        boxplot['means'][0].set_label('mean')
        boxplot['fliers'][0].set_label('outlayers')
        # boxplot['boxes'][0].set_label('boxes')
        # boxplot['whiskers'][0].set_label('whiskers')
        boxplot['caps'][0].set_label('caps')

        axes.set_xlim([0.7, 1.7])

        plt.legend(numpoints = 1)

    zoomOutY(axes,factor=0.1)
    axes.set_title(title)

def plotMultipleWhiskerPlots(datas, whiskers, labels):
    # support of generating multiple box plots
    '''
    Example run:

    means_men = (20, 35, 30, 35, 27)
    std_men = (2, 3, 4, 1, 2)
    means_women = (25, 32, 34, 20, 25)
    std_women = (3, 5, 2, 3, 3)

    datas = [means_men, means_women, means_men]
    whiskers = [std_men, std_women, std_women]
    labels = ['1', '2', '3']

    plotMultipleWhiskerPlots(datas,whiskers,labels)
    '''
    fig, ax = plt.subplots()

    index = np.arange(len(datas[0]))
    bar_width = (1.0 / len(datas)) * 0.9

    opacity = 0.6
    error_config = {'ecolor': '0.3'}

    colors = ['r', 'b', 'y']

    for i in range(0,len(datas)):
        rects = plt.bar(index + i*bar_width, datas[i], bar_width,
                         alpha=opacity,
                         color=colors[min(i,len(colors)-1)],
                         yerr=whiskers[i],
                         error_kw=error_config,
                         label=labels[i])

    plt.xticks(index + bar_width / len(datas),np.arange(1,len(datas[0])+1))
    plt.legend()
    plt.tight_layout()

def subPlot2(fce1, fce2, param1=None, param2=None):
    '''
    Join two plots.

    Example run:
    def tmp_fce1(): ...
    def tmp_fce2(): ...
    subPlot2(tmp_fce1, tmp_fce2)
    '''
    plt.subplot(2, 1, 1)
    fce1()
    plt.subplot(2, 1, 2)
    fce2()
    plt.show()

def zoomOut(axes, xlim=None, ylim=None, factor=0.05):
    '''
    Set size to fit in limitations.
    :param axes: handler to matlibplot
    :param xlim: list of [from x, to x] values
    :param ylim: list of [from y, to y] values
    :param factor: zoom factor
    :return:
    '''
    zoomOutX(axes, xlim, factor)
    zoomOutY(axes, ylim, factor)

def zoomOutX(axes,xlim=None,factor=0.05):
    # handle the X axis
    if xlim == None:
        xlim = axes.get_xlim()
    axes.set_xlim((xlim[0] + xlim[1]) / 2 + np.array((-0.5, 0.5)) * (xlim[1] - xlim[0]) * (1 + factor))
def zoomOutY(axes,ylim=None,factor=0.05, only_up = False):
    # handle the Y axis
    if ylim == None:
        ylim = axes.get_ylim()
    bottom = -0.5
    axes.set_ylim((ylim[0] + ylim[1]) / 2 + np.array((-0.5, 0.5)) * (ylim[1] - ylim[0]) * (1 + factor))
    if only_up:
        ylim = axes.get_ylim()
        #print ylim
        axes.set_ylim(0.0,ylim[1])

