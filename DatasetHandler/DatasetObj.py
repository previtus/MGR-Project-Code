import Downloader.DataOperations as DataOperations
import Downloader.KerasPreparation as KerasPreparation
import os
import shutil
import numpy as np
import random
import math
import Downloader.Defaults
from Omnipresent import file_exists_and_accesible

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
    flag_is_extended = False

    def __init__(self):
        return None

    def randomize_all_list_order_deterministically_same_segment(self, local_seed):
        '''
        According to a chosen seed number will shuffle contents of lists (of urls, of scores, of osm) so they are kept
         intact.
        :return:
        '''

        n = len(self.__list_of_images)
        indices = range(0,n)
        #indices = range(0,n)*6
        #indices += range(0,n)

        a = self.__list_of_images
        b = self.__labels
        c = self.__osm
        d = self.__segment_ids

        #print len(a), len(b), len(c), len(d), d[0:10]

        lists = list(zip(a, b, c, d))
        shuffled_lists = []
        already_used_data = []

        random.Random(local_seed).shuffle(indices)
        for index in indices:
            if index in already_used_data:
                continue

            str_ = ''
            l = lists[index]
            seg_id = l[3]

            #print index, seg_id, l

            #for k in range(-6,6):
            #    print index+k, lists[index+k][3]

            k = index-1
            found_first_of_such_id = False
            if k == -1:
                found_first_of_such_id = True
            while not found_first_of_such_id:
                seg_id_prev = lists[k][3]
                if seg_id == seg_id_prev:
                    k -= 1
                else:
                    k += 1
                    found_first_of_such_id = True

            first_index = k
            last_index = k

            found_last_of_such_id = False
            k += 1
            while not found_last_of_such_id:
                if k >= n:
                    found_last_of_such_id = True
                    last_index = k-1
                elif seg_id == lists[k][3]:
                    k += 1
                else:
                    found_last_of_such_id = True
                    last_index = k-1

            str_ = ''
            for i in range(first_index, last_index+1):
                #print i, lists[i][3]
                str_ += str(i)+'('+str(lists[i][3])+'), '
                shuffled_lists.append(lists[i])
                already_used_data.append(i)
            #print str_
            #print 'pre', first_index-1, lists[first_index-1][3]
            #print 'post', last_index+1, lists[last_index+1][3]

            '''
            for k in range(0,images_per_segment):
                index = i*images_per_segment+k
                str_ += str(i*images_per_segment+k)+', '
                shuffled_lists.append(lists[index])
            #print str_
            '''

        a, b, c, d = zip(*shuffled_lists)
        self.__list_of_images = a
        self.__labels = np.array(b)
        self.__osm = c
        self.__segment_ids = d

        #print len(a), len(b), len(c), len(d), d[0:10]

    def remove_dual_osms(self):
        '''
        We know that every third entry is actually unique (in sense of osm,score pair) - when we are talking about osm_only model
        :return:
        '''
        indices = []

        images_per_segment = 3
        n = len(self.__list_of_images)
        bytripples = range(0,int(n/images_per_segment))

        for i in bytripples:
            indices.append(i*images_per_segment)

        print len(self.__list_of_images), len(self.__labels), len(self.__osm), len(self.__segment_ids)
        self.__list_of_images = [self.__list_of_images[i] for i in indices]
        self.__labels = [self.__labels[i] for i in indices]
        self.__osm = [self.__osm[i] for i in indices]
        self.__segment_ids = [self.__segment_ids[i] for i in indices]

        print len(self.__list_of_images), len(self.__labels), len(self.__osm), len(self.__segment_ids)

    def test_existence_of_all_images(self):
        '''
        Test physical presence of the images - useful for debuging.
        :return:
        '''
        for url in self.__list_of_images:
            b = file_exists_and_accesible(url)
            if not b:
                print "File cannot be accessed! ", url

    def init_from_lists(self, list_of_images, labels, osm, segment_ids, img_width, img_height):
        '''
        Initialization from lists of data
        '''
        self.img_width = img_width
        self.img_height = img_height
        self.__list_of_images = list_of_images
        self.__labels = labels
        self.__osm = osm
        self.__segment_ids = segment_ids
        self.num_of_images = len(self.__list_of_images)

        self.has_osm_loaded = (len(self.__osm)>0)

    def init_from_segments(self, path_to_segments_file, img_width, img_height):
        '''
        # Initialization from loaded Segment in path_to_segments_file
        # Segments are not used apart from initialization
        '''
        Segments = DataOperations.LoadDataFile(path_to_segments_file)
        segments_dir = os.path.dirname(path_to_segments_file) + '/'
        __list_of_images, __labels, __osm, __segment_ids, flag_is_extended = KerasPreparation.LoadDataFromSegments(Segments, has_score=True, path_to_images=segments_dir)
        self.flag_is_extended = flag_is_extended

        self.init_from_lists(__list_of_images, __labels, __osm, __segment_ids, img_width, img_height)

    # Osm data editation
    def cast_osm_to_bool(self):
        '''
        Transforms the osm vector data to boolean values, aka i=0 -> 0, i>0 -> 1
        :return:
        '''

        def boo(x):
            if x > 0:
                return 1
            else:
                return 0
        for i in range(len(self.__osm)):
            for j in range(len(self.__osm[i])):
                self.__osm[i][j] = boo(self.__osm[i][j])

    def cast_osm_to_one_hot_categories(self):
        '''
        Transforms the osm vector data to one hot categories - low,mid,high represented as 001,010,100 binary.
        :return:
        '''
        if len(self.__osm) == 0:
            return False

        statistics_for_attributes = []

        for attribute_id in range(len(self.__osm[0])):
            attribute_values = []
            for vector_id in range(len(self.__osm)):
                val = self.__osm[vector_id][attribute_id]
                attribute_values.append(val)

            q1 = np.percentile(attribute_values, 33)
            q3 = np.percentile(attribute_values, 66)

            #print attribute_id, q1, q3
            statistics_for_attributes.append([q1, q3])

        new_osm_vector = []
        for vector_id in range(len(self.__osm)):
            new_osm_vector.append([])
            for attribute_id in range(len(self.__osm[vector_id])):
                stats = statistics_for_attributes[attribute_id]
                val = self.__osm[vector_id][attribute_id]

                if val <= stats[0]: # value smaller than lower percentile -> "low"
                    new_osm_vector[vector_id] += [0,0,1]
                elif val <= stats[1]: # value in between percentiles -> "mid"
                    new_osm_vector[vector_id] += [0,1,0]
                else: # bigger than percentiles -> "high"
                    new_osm_vector[vector_id] += [1,0,0]

        self.__osm = new_osm_vector

    def log_the_osm(self):
        '''
        Apply log to values in OSM vector.
        :return:
        '''
        for i in range(len(self.__osm)):
            for j in range(len(self.__osm[i])):
                val = self.__osm[i][j]
                if val > 1:
                    val = math.log(val)

                self.__osm[i][j] = val

    # Data access: ---------------------------------------------------------------------------------------------
    def getDataLabels(self, resize=None):
        '''
        # ([x,y]) as image data and labels
        '''
        x = KerasPreparation.LoadActualImages(self.__list_of_images, resize=resize, dim_ordering=Downloader.Defaults.KERAS_SETTING_DIMENSIONS)
        y = np.array(self.__labels)
        return [x, y]

    def getDataLabels_split(self, resize=None, validation_split=0.2):
        '''
        # ([x, y, x_val, y_val]) as image data and labels after being split
        '''
        x = KerasPreparation.LoadActualImages(self.__list_of_images, resize=resize, dim_ordering=Downloader.Defaults.KERAS_SETTING_DIMENSIONS) # th or tf
        y = np.array(self.__labels)

        x, y, x_val, y_val = KerasPreparation.split_data(x, y, validation_split)
        return [x, y, x_val, y_val]

    def getDataLabels_split_only_y(self, resize=None, validation_split=0.2):
        '''
        # Get just label data, after validation split
        '''
        y = np.array(self.__labels)
        y, y_val = KerasPreparation.split_one_array(y, validation_split)
        return [y, y_val]

    def getDataLabels_only_y(self):
        '''
        # Get just label data
        '''
        y = np.array(self.__labels)
        return y

    def getDataLabels_split_only_osm(self, validation_split=0.2):
        '''
        # Get just osm data, after validation split
        '''
        osm, osm_val = KerasPreparation.split_one_array(self.__osm, validation_split)
        osm = np.asarray(osm)
        osm_val = np.asarray(osm_val)

        return [osm, osm_val]

    def getDataLabels_only_osm(self):
        '''
        # Get just osm data
        '''
        osm = np.array(self.__osm)
        return osm

    def getShapeOfOsm(self):
        '''
        Get shape of the osm data - aka dimension of the vectors, traditionally (594,) needed for building Keras models.
        :return:
        '''
        return np.asarray(self.__osm).shape[1:]

    # For generators
    def generator_images_scores(self, order, image_paths, scores, resize=None):
        '''
        Get generator of images
        :param order: prearanged order (1,2,3...) or (2,55,1,980, ...)
        :param image_paths: paths to images, these are kept in memory while the big 640x640x3 image data is not
        :param scores: score to be associated with returned image
        :param resize: parameter to resize loaded images on the fly
        :return: generator, which yields (image, score)
        '''
        while True:
            for index in order:
                img_path = image_paths[index]

                image = KerasPreparation.LoadActualImages([img_path], resize=resize)
                score = scores[index]
                yield (image, score)

    def getImageGenerator(self, validation_split, resize=None):
        '''
        # Return generators
        # take the lists on images and their labels - split these two arrays by the validation split
        '''
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

    # Dataset reporting: ---------------------------------------------------------------------------------------------

    def statistics(self):
        '''
        # Report important information about the dataset.
        '''
        print "Dataset of", len(self.__list_of_images), " scored images of", self.img_width, "x", self.img_height, "resolution."
        labels = np.array(self.__labels)
        min = np.amin(labels)
        max = np.amax(labels)
        mean = np.mean(labels)
        q1 = np.percentile(labels, 25)
        q3 = np.percentile(labels, 75)
        print min, "|---[", q1, "{", mean, "}", q3, "]---|", max
        print "min |---[ 25perc { mean } 75perc ]---| max"

    def debug_print_first(self, n):
        '''
        # Debug print first n values in this dataset.
        '''
        for i in range(0,n):
            print self.__segment_ids[i], self.__labels[i], self.__list_of_images[i]


    def plotHistogram(self, save_to_pdf=False, labels_override=None):
        '''
        Plot score of this dataset as histogram.
        :param save_to_pdf: flag to save into output.pdf
        :return:
        '''
        import DatasetVizualizators

        if labels_override is not None:
            labels = np.array(self.__labels)
        else:
            labels = labels_override
        DatasetVizualizators.plotHistogram(labels, 'Score distribution histogram')
        DatasetVizualizators.plotWhisker(labels, 'Score box plot')
        DatasetVizualizators.plotX_sortValues(labels, 'Distribution of score (sorted)', notReverse=True)
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

    def DumpFilesIntoDirectory_keepNamesOnlyScored(self, target_directory = ''):
        """
        Copy those images which are loaded to this database and thus also have score into another folder.
        This can be used to filter how much of the initial dataset is useful as labeled dataset.
        :param target_directory: target folder, file names are kept the same
        """

        if not os.path.exists(target_directory):
            os.makedirs(target_directory)

        for i in range(0, self.num_of_images):
            name = self.__list_of_images[i]
            score = self.__labels[i]

            #head, tail = os.path.split(name)

            filename = target_directory + "/" + os.path.basename(name)

            print name, score, filename

            shutil.copy2(name, filename)

    def build_dictionary_instead_of_object(self, include_osms=False):
        """
        Output all the knowledge of labels of this dataset into dictionary which can give label from id, which is the
        name of the file (0123_0<?>.jpg, keep in mind that further processing can add more into <?>).

        File name goes as first 4 numbers 0123, underscore and more numbers. The first set corresponds to the id of
        segment, thus one unique road. It has the same score for all variants which are created when rotating around
        the spot and generating other images. However these can have variable osm data (as the "center" where we were
        standing was differing).

        USE LIKE THIS:
        np.save('id_to_score.npy', dictionary)
        dict_loaded = np.load('id_to_score.npy').item()

        // if we have scores only, we can look at them like histogram like this:
        list1 = d1.values()
        flat_list = [item for sublist in list1 for item in sublist]
        // ...

        :param include_osms: Flag if we also keep osm data
        :return:
        """

        dictionary_id_to_labels = {}

        for i in range(0, self.num_of_images):
        #for i in range(0, 5):
            name = self.__list_of_images[i]
            seq = name.split("/")
            file_name_id = seq[-1][0:-4]
            score = self.__labels[i]

            if include_osms:
                osm = self.__osm[i]
                dictionary_id_to_labels[file_name_id] = [score, osm]
            else:
                dictionary_id_to_labels[file_name_id] = [score]

        return dictionary_id_to_labels

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

    def sampleUniform(self, desired_number):
        '''
        # randomized subsample of a dataset
        '''
        indices = random.sample(xrange(self.num_of_images), desired_number)
        return indices

    def spawnUniformSubset(self, desired_number):
        '''
        Spawn a subset from dataset uniform distribution over the original data.

        :param desired_number: size of the desired dataset
        :return: the resulting new dataset
        '''
        indices = self.sampleUniform(desired_number)

        sel_imgs = [self.__list_of_images[i] for i in indices]
        sel_labels = [self.__labels[i] for i in indices]
        sel_segment_ids = [self.__segment_ids[i] for i in indices]

        if self.__osm == []:
            sel_osm = []
        else:
            sel_osm = [self.__osm[i] for i in indices]

        newDataset = Dataset()
        newDataset.init_from_lists(sel_imgs, sel_labels, sel_osm, sel_segment_ids, self.img_width, self.img_height)

        return newDataset

    def getDataLabels_only_osm_raw(self):
        '''
        # return list of osm without coversion to numpy format
        '''
        return self.__osm

    def expandOsmDataWithMultipleRadii(self, model_settings):
        '''
        # idea is to load all the radii data we have available and add it to each of the segments
        # we assume the basic experiment definition
        '''
        r50 = 'SegmentsData_marked_R50_4TablesN.dump'
        r100 = 'SegmentsData_marked_R50_4TablesN.dump'
        r200 = 'SegmentsData_marked_R200_4TablesN.dump'

        import DatasetHandler
        dataset_r50 = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                                                           desired_number=model_settings["number_of_images"],
                                                           seed=model_settings["seed"],
                                                           filename_override=r50)
        r50osm = dataset_r50.getDataLabels_only_osm_raw()
        dataset_r100 = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                                                           desired_number=model_settings["number_of_images"],
                                                           seed=model_settings["seed"],
                                                           filename_override=r100)
        r100osm = dataset_r100.getDataLabels_only_osm_raw()
        dataset_r200 = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                                                           desired_number=model_settings["number_of_images"],
                                                           seed=model_settings["seed"],
                                                           filename_override=r200)
        r200osm = dataset_r200.getDataLabels_only_osm_raw()

        from Omnipresent import len_
        print "osm", len(self.__osm), len_(self.__osm), self.__osm[0][0:10]
        print "osm50", len(r50osm), len_(r50osm), r50osm[0][0:10]
        print "osm50", len(r100osm), len_(r100osm), r100osm[0][0:10]
        print "osm200", len(r200osm), len_(r200osm), r200osm[0][0:10]

        new_osm = []
        for i in range(0,len(r50osm)):
            osm_of_i = []
            if model_settings["multiple_radii_mark"] == 'I':
                osm_of_i = list(r100osm[i]) + list(r50osm[i]) + list(r200osm[i])
            elif model_settings["multiple_radii_mark"] == 'II':
                osm_of_i = list(r100osm[i]) + list(r200osm[i])
            elif model_settings["multiple_radii_mark"] == 'III':
                osm_of_i = list(r100osm[i]) + list(r50osm[i])

            new_osm.append(osm_of_i)

        print "enhanced", len(new_osm), len_(new_osm), new_osm[0][0:10]
        self.__osm = new_osm
        print "enhanced", len(self.__osm), len_(self.__osm), self.__osm[0][0:10]
