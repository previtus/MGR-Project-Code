import Downloader.DataOperations as DataOperations
import Downloader.KerasPreparation as KerasPreparation
import os
import copy
import numpy as np
import DatasetVizualizators

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

    segments_filename = ''
    segments_dir = ''
    __Segments = []
    __list_of_images = []
    __labels = []
    img_width = -1
    img_height = -1
    num_of_images = 0

    def __init__(self, path_to_segments_file, img_width, img_height):
        self.segments_filename = path_to_segments_file
        self.segments_dir = os.path.dirname(path_to_segments_file)+'/'
        self.img_width = img_width
        self.img_height = img_height

        # load Segments for internal use here
        self.__Segments = DataOperations.LoadDataFile(self.segments_filename)
        self.__list_of_images, self.__labels = KerasPreparation.LoadDataFromSegments(self.__Segments, has_score=True, path_to_images=self.segments_dir)

        self.num_of_images = len(self.__list_of_images)

    # Data access: ---------------------------------------------------------------------------------------------

    def getDataLabels(self):
        # ([x],[y]) as image data and labels
        x = KerasPreparation.LoadActualImages(self.__list_of_images)
        y = self.__labels
        return [x, y]

    def getDataLabels_split(self, validation_split=0.2):
        # ([x],[y]) as image data and labels
        x = KerasPreparation.LoadActualImages(self.__list_of_images)
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

        print self.__labels
        x = copy.copy(self.__labels)
        x.sort(reverse=True)
        print x
        print len(x)

    def plotHistogram(self):
        DatasetVizualizators.plotHistogram(self.__labels, 'Score distribution histogram')
        DatasetVizualizators.plotWhisker(self.__labels, 'Whisker box plot')
        DatasetVizualizators.plotX_sortValues(self.__labels, 'Distribution of score (sorted)')
        DatasetVizualizators.show()


#path = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/Data/StreetViewData/TestData/SegmentsData.dump'
#path = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/Downloader/SegmentsData.dump'
path = '../Downloader/SegmentsData.dump'

testDataset = Dataset(path, 640, 640)
testDataset.statistics()
# cetnosti 12 6 6
testDataset.plotHistogram()
