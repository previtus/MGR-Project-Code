import Downloader.DataOperations as DataOperations
import Downloader.KerasPreparation as KerasPreparation
import os
import shutil
import numpy as np
import random
import Downloader.Defaults

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
    __osm = []
    img_width = -1
    img_height = -1
    num_of_images = 0
    unique_id = ''
    has_osm_loaded = False

    def __init__(self):
        return None

    def randomize_all_list_order_deterministically(self, local_seed):
        '''
        According to a chosen seed number will shuffle contents of lists (of urls, of scores, of osm) so they are kept
         intact.
        :return:
        '''

        a = self.__list_of_images
        b = self.__labels
        c = self.__osm

        lists = list(zip(a, b, c))
        random.Random(local_seed).shuffle(lists)

        a, b, c = zip(*lists)
        self.__list_of_images = a
        self.__labels = np.array(b)
        self.__osm = c

    def randomize_all_list_order_deterministically_modulo(self, local_seed):
        '''
        According to a chosen seed number will shuffle contents of lists (of urls, of scores, of osm) so they are kept
         intact.
        :return:
        '''

        images_per_segment = 6
        n = len(self.__list_of_images)
        indices = range(0,int(n/images_per_segment))
        #print indices
        #print n, self.__list_of_images


        a = self.__list_of_images
        b = self.__labels
        c = self.__osm

        lists = list(zip(a, b, c))
        shuffled_lists = []

        random.Random(local_seed).shuffle(indices)
        for i in indices:
            str_ = ''
            for k in range(0,images_per_segment):
                index = i*images_per_segment+k
                str_ += str(i*images_per_segment+k)+', '
                shuffled_lists.append(lists[index])
            #print str_

        a, b, c = zip(*shuffled_lists)
        self.__list_of_images = a
        self.__labels = np.array(b)
        self.__osm = c


    def init_from_lists(self, list_of_images, labels, osm, img_width, img_height):
        self.img_width = img_width
        self.img_height = img_height
        self.__list_of_images = list_of_images
        self.__labels = labels
        self.__osm = osm
        self.num_of_images = len(self.__list_of_images)

        self.has_osm_loaded = (len(self.__osm)>0)

    def init_from_segments(self, path_to_segments_file, img_width, img_height):
        # Segments are not used apart from initialization
        Segments = DataOperations.LoadDataFile(path_to_segments_file)
        segments_dir = os.path.dirname(path_to_segments_file) + '/'
        __list_of_images, __labels, __osm = KerasPreparation.LoadDataFromSegments(Segments, has_score=True, path_to_images=segments_dir)

        self.init_from_lists(__list_of_images, __labels, __osm, img_width, img_height)

    # Osm data editation
    def cast_osm_to_bool(self):
        '''
        Transforms the osm vector data to boolean values, aka i=0 -> 0, i>0 -> 1
        :return:
        '''

        #print self.__osm[0][0:30]

        def boo(x):
            if x > 0:
                return 1
            else:
                return 0
        for i in range(len(self.__osm)):
            for j in range(len(self.__osm[i])):
                self.__osm[i][j] = boo(self.__osm[i][j])
            #self.__osm[i] = [boo(x) for x in self.__osm[i]]

        #print self.__osm[0][0:30]

    # Data access: ---------------------------------------------------------------------------------------------
    def getJustLabels(self, validation_split=0.2):
        y = np.array(self.__labels)
        y, y_val = KerasPreparation.split_one_array(y, validation_split)
        return [y, y_val]

    def getDataLabels(self, resize=None):
        # ([x],[y]) as image data and labels
        x = KerasPreparation.LoadActualImages(self.__list_of_images, resize=resize, dim_ordering=Downloader.Defaults.KERAS_SETTING_DIMENSIONS)
        y = np.array(self.__labels)
        return [x, y]

    def getDataLabels_split(self, resize=None, validation_split=0.2):
        # ([x],[y]) as image data and labels
        x = KerasPreparation.LoadActualImages(self.__list_of_images, resize=resize, dim_ordering=Downloader.Defaults.KERAS_SETTING_DIMENSIONS) # th or tf
        y = np.array(self.__labels)

        x, y, x_val, y_val = KerasPreparation.split_data(x, y, validation_split)
        return [x, y, x_val, y_val]

    def getDataLabels_split_only_y(self, resize=None, validation_split=0.2):
        y = np.array(self.__labels)
        y, y_val = KerasPreparation.split_one_array(y, validation_split)
        return [y, y_val]

    def getDataLabels_split_only_osm(self, validation_split=0.2):
        osm, osm_val = KerasPreparation.split_one_array(self.__osm, validation_split)
        osm = np.asarray(osm)
        osm_val = np.asarray(osm_val)

        return [osm, osm_val]

    def getDataLabels_split_with_osm(self, resize=None, validation_split=0.2):
        [x, y, x_val, y_val] = self.getDataLabels_split(resize, validation_split)
        osm, osm_val = KerasPreparation.split_osm(self.__osm,validation_split)

        return [x, y, x_val, y_val, osm, osm_val]

    def getShapeOfOsm(self):
        return np.asarray(self.__osm).shape[1:]

    # For generators
    def generator_images_scores(self, order, image_paths, scores, resize=None):
        # possibly: change it to give batches of predefined sizes, like batch_size = 32

        while True:
            for index in order:
                img_path = image_paths[index]

                image = KerasPreparation.LoadActualImages([img_path], resize=resize)
                score = scores[index]
                yield (image, score)

    def generator_features_osm_scores(self, order, all_features, osm_vectors, scores):

        while True:
            for index in order:
                score = scores[index]
                features = all_features[index]

                #osm_vector = osm_vectors[index]
                #yield ([osm_vector, features], score)
                #yield np.asarray(features), np.asarray(score)
                yield [features, score]

                #yield (features, score)
                #yield (np.array([features]), score)

    def generator_triple_with_enhancement(self, order, image_paths, scores, osms, resize=None):
        # yield ([image, osm], score)

        # Somehow include datagen = ImageDataGenerator(...)
        # batches = datagen.flow( ... ) so it gives us all what we need

        while True:
            for index in order:
                img_path = image_paths[index]

                image = KerasPreparation.LoadActualImages([img_path], resize=resize)
                score = scores[index]
                osm = osms[index]
                yield ([image, osm], score)

    def getImageGenerator(self, validation_split, resize=None):
        # idea:
        # take the lists on images and their labels - split these two arrays by the validation split
        y = np.array(self.__labels)
        images_paths, scores, images_paths_val, scores_val = KerasPreparation.split_data(self.__list_of_images, y, validation_split)

        size = len(scores)
        size_val = len(scores_val)

        order = range(size)
        order_val = range(size_val)
        # We can mix up the orders, but then we need to mix the future data too

        image_generator = self.generator_images_scores(order, image_paths=images_paths, scores=scores, resize=resize)
        image_generator_val = self.generator_images_scores(order_val, image_paths=images_paths_val, scores=scores_val, resize=resize)

        return [order, order_val, image_generator, size, image_generator_val, size_val]

        # [test_generator, val_generator, number_in_test, number_in_val]

    def getFeatureGenerator(self, order, order_val, validation_split, features, features_val):
        #osm, osm_val = KerasPreparation.split_one_array(self.__osm, validation_split)
        osm=[]
        osm_val=[]
        y = np.array(self.__labels)
        scores, scores_val = KerasPreparation.split_one_array(y, validation_split)

        feature_generator = self.generator_features_osm_scores(order, features, osm_vectors=osm, scores=scores)

        feature_generator_val = self.generator_features_osm_scores(order_val, features_val, osm_vectors=osm_val,
                                                               scores=scores_val)

        size = len(scores)
        size_val = len(scores_val)
        return [feature_generator, feature_generator_val, size, size_val]

    # Dataset reporting: ---------------------------------------------------------------------------------------------

    def statistics(self):
        print "Dataset of", self.num_of_images, " scored images of", self.img_width, "x", self.img_height, "resolution."
        labels = np.array(self.__labels)
        min = np.amin(labels)
        max = np.amax(labels)
        mean = np.mean(labels)
        q1 = np.percentile(labels, 25)
        q3 = np.percentile(labels, 75)
        print min, "|---[", q1, "{", mean, "}", q3, "]---|", max
        print "min |---[ 25perc { mean } 75perc ]---| max"

        #print labels
        #x = copy.copy(labels)
        #x.sort(reverse=True)
        #print x
        #print len(x)

    def plotHistogram(self, save_to_pdf=False):
        import DatasetVizualizators
        labels = np.array(self.__labels)
        DatasetVizualizators.plotHistogram(labels, 'Score distribution histogram')
        DatasetVizualizators.plotWhisker(labels, 'Whisker box plot')
        DatasetVizualizators.plotX_sortValues(labels, 'Distribution of score (sorted)')
        if save_to_pdf:
            DatasetVizualizators.saveAllPlotsToPDF()
        DatasetVizualizators.show()

    def MapScoreToImages(self, into_bins=100):
        '''
        Gets a dict which give to a index from 0-100 a list of images of such score (score goes in range 0-1, so *100 in this case)
        :return:
        '''
        into_bins -= 1
        # Empty dict
        dict = {key: [] for key in range(0,into_bins+1)}

        for i in range(0, self.num_of_images):
            name = self.__list_of_images[i]
            score = float(self.__labels[i])
            score_label = int(round(score, 2)*100)

            score_label = int(score_label*into_bins/100)

            dict[score_label].append(name)
        return dict

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
        # this is without repetition
        #print self.num_of_images, desired_number

        indices = random.sample(xrange(self.num_of_images), desired_number)

        #print indices
        return indices

    # TODO sample wanted number of images, so that the resulting set is uniform with its scores
    '''
    def sampleUniformNumberOfImagesPerScore(self, desired_number=0):
        X = self.__list_of_images
        Y = self.__labels
        sorted_list_of_images = [x for (y, x) in sorted(zip(Y, X), key=lambda pair: pair[0])]
        sorted_labels = copy.copy(Y)
        sorted_labels.sort()

        for i in range(0,len(sorted_labels)):
            print sorted_labels[i], sorted_list_of_images[i]

        # not yet done, dont know if we need it

        return [] #[sorted_list_of_images, sorted_labels]
    '''

    def spawnUniformSubset(self, desired_number):
        '''
        Spawn a subset from dataset uniform distribution over the original data.

        :param desired_number: size of the desired dataset
        :return: the resulting new dataset
        '''
        indices = self.sampleUniform(desired_number)

        sel_imgs = [self.__list_of_images[i] for i in indices]
        sel_labels = [self.__labels[i] for i in indices]

        if self.__osm == []:
            sel_osm = []
        else:
            sel_osm = [self.__osm[i] for i in indices]

        newDataset = Dataset()
        newDataset.init_from_lists(sel_imgs, sel_labels, sel_osm, self.img_width, self.img_height)

        return newDataset

