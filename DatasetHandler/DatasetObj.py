import Downloader.DataOperations as DataOperations
import Downloader.KerasPreparation as KerasPreparation
import os
import copy
import shutil
import numpy as np
import DatasetVizualizators
import random

class Dataset:
    '''
    Common base class for a Dataset

    What does dataset have?

     - source data folder with images and their scores - via Segments, but we don't use Segments anymore anywhere out

    What can it do?

     - give it's data nicely out ([x],[y]) as image data and labels
     - give us subsets, which are uniform in sense of Scoring
     - provide us with statistics - without worrying about unsuccessful downloads or anything
     - give us *views* like exporting images into folder for inspection - for example coded with score

    '''

    __list_of_images = []
    __labels = []
    img_width = -1
    img_height = -1
    num_of_images = 0

    def __init__(self):
        return None

    def init_from_lists(self, list_of_images, labels, img_width, img_height):
        self.img_width = img_width
        self.img_height = img_height
        self.__list_of_images = list_of_images
        self.__labels = labels
        self.num_of_images = len(self.__list_of_images)

    def init_from_segments(self, path_to_segments_file, img_width, img_height):
        # Segments are not used apart from initialization
        Segments = DataOperations.LoadDataFile(path_to_segments_file)
        segments_dir = os.path.dirname(path_to_segments_file) + '/'
        __list_of_images, __labels = KerasPreparation.LoadDataFromSegments(Segments, has_score=True, path_to_images=segments_dir)

        self.init_from_lists(__list_of_images, __labels, img_width, img_height)

    # Data access: ---------------------------------------------------------------------------------------------

    def getDataLabels(self, resize=None):
        # ([x],[y]) as image data and labels
        x = KerasPreparation.LoadActualImages(self.__list_of_images, resize=resize)
        y = self.__labels
        return [x, y]

    def getDataLabels_split(self, resize=None, validation_split=0.2):
        # ([x],[y]) as image data and labels
        x = KerasPreparation.LoadActualImages(self.__list_of_images, resize=resize)
        y = self.__labels

        x, y, x_val, y_val = KerasPreparation.split_data(x, y, validation_split)
        return [x, y, x_val, y_val]

    # Dataset reporting: ---------------------------------------------------------------------------------------------

    def statistics(self):
        print "Dataset of", self.num_of_images, " scored images of", self.img_width, "x", self.img_height, "resolution."
        min = np.amin(self.__labels)
        max = np.amax(self.__labels)
        mean = np.mean(self.__labels)
        q1 = np.percentile(self.__labels, 25)
        q3 = np.percentile(self.__labels, 75)
        print min, "|---[", q1, "{", mean, "}", q3, "]---|", max
        print "min |---[ 25perc { mean } 75perc ]---| max"

        #print self.__labels
        #x = copy.copy(self.__labels)
        #x.sort(reverse=True)
        #print x
        #print len(x)

    def plotHistogram(self, save_to_pdf=False):
        DatasetVizualizators.plotHistogram(self.__labels, 'Score distribution histogram')
        DatasetVizualizators.plotWhisker(self.__labels, 'Whisker box plot')
        DatasetVizualizators.plotX_sortValues(self.__labels, 'Distribution of score (sorted)')
        if save_to_pdf:
            DatasetVizualizators.saveAllPlotsToPDF()
        DatasetVizualizators.show()

    def DumpFilesIntoDirectory_withScores(self, target_directory = ''):
        '''
        Simple way of visualizing which images are considered "attractive" (with high score) and which are not
        :param target_directory: target directory, for example target_directory = '../debugViewOfDataset/'
        :return: returns list of new names of files, with the order unchanged
        '''
        # Copy images from their original location to a new directory while naming them:
        # Score_<OriginalName.jpg>
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        new_names = []
        for i in range(0, self.num_of_images):
            name = self.__list_of_images[i]
            score = self.__labels[i]

            #head, tail = os.path.split(name)

            filename = target_directory + "{0:.2f}".format(score) + '_' + os.path.basename(name)

            #print name, score, filename
            new_names.append(filename)

            shutil.copy2(name, filename)
        return new_names

    def DebugGetDatasetArrays(self):
        return [self.__list_of_images, self.__labels]

    def sampleUniform(self, desired_number):
        indices = random.sample(xrange(self.num_of_images), desired_number)


