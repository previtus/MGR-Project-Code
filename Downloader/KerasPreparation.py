from ImageHelpers import *
from keras.preprocessing.image import ImageDataGenerator

from Defaults import *
from DataOperations import *
from PreprocessData.SegmentsManipulators import *

def split_one_array(arr,validation_split=0.2):
    '''
    :param arr: list of data to be split
    :param validation_split: Split ratio, defaults to 80% for test set and 20% of validation set
    :return: Returns split data
    '''
    if not(0 < validation_split < 1):
        print "Choose validation_split in between 0 and 1. Setting the default value of 0.2"
        validation_split = 0.2

    split_at = int(len(arr) * (1 - validation_split))
    arr_train = arr[0:split_at]
    arr_val = arr[split_at:]
    return arr_train,arr_val

def split_data(x,y,validation_split=0.2):
    '''
    :param x: Dataset, can be paths to images or directly the image data for example (?, 3,222,222)
    :param y: Labels of the datasets
    :param validation_split: Split ratio, defaults to 80% for test set and 20% of validation set
    :return: Returns split data
    '''
    if not(0 < validation_split < 1):
        print "Choose validation_split in between 0 and 1. Setting the default value of 0.2"
        validation_split = 0.2

    split_at = int(len(x) * (1 - validation_split))
    x_test = x[0:split_at]
    y_test = y[0:split_at]
    x_val = x[split_at:]
    y_val = y[split_at:]

    #print "Split", len(x), "images into", len(x_test), "test and", len(x_val), "validation sets."
    return x_test,y_test,x_val, y_val

def split_osm(osm,validation_split=0.2):
    '''
    Split array of osm vectors by validation split.
    :param osm: osm data
    :param validation_split: 0 to 1 fraction
    :return: splitted osm data into osm_test, osm_val
    '''
    if not(0 < validation_split < 1):
        print "Choose validation_split in between 0 and 1. Setting the default value of 0.2"
        validation_split = 0.2

    split_at = int(len(osm) * (1 - validation_split))
    osm_test = osm[0:split_at]
    osm_val = osm[split_at:]
    return osm_test, osm_val

def LoadDataFromSegments(Segments, has_score=True, path_to_images=None, we_dont_care_about_missing_images=False):
    '''
    Turns loaded segments into data we will need for keras.
    :param Segments: Loaded segments
    :param path_to_images: additional path specification which we need before 'images/---.jpg'
    :return: Returns list of urls of images and their labels (score in the Segment)
    '''
    list_of_images = []
    labels = []
    osm_vectors = []
    segment_ids = []

    segment_id = 0
    flag_is_extended = False

    '''
    number_no_score_yes_img = 0
    number_no_score_no_img = 0
    number_yes_score_yes_img = 0
    number_yes_score_no_img = 0
    '''
    for Segment in Segments:

        '''
        # stats:
        if Segment.hasUnknownScore():
            for i_th_image in range(0,Segment.number_of_images):
                if Segment.hasLoadedImageI(i_th_image):
                    number_no_score_yes_img += 1
                else:
                    number_no_score_no_img += 1
        else:
            for i_th_image in range(0,Segment.number_of_images):
                if Segment.hasLoadedImageI(i_th_image):
                    number_yes_score_yes_img += 1
                else:
                    number_yes_score_no_img += 1
        '''


        # if we care for score
        if (has_score and not Segment.hasUnknownScore()) or (has_score == None):
            # but we always care for images
            for i_th_image in range(0,Segment.number_of_images):
                location_index = Segment.LocationsIndex[i_th_image]

                is_extended = False
                if location_index > 500:
                    # then this particular image is loaded from an extended folder
                    is_extended = True
                    location_index -= 1000
                    flag_is_extended = True
                if Segment.hasLoadedImageI(i_th_image) or (we_dont_care_about_missing_images):

                    filename = Segment.getImageFilename(i_th_image)
                    if is_extended:
                        filename = 'images' + filename[6:]

                    list_of_images.append(filename)
                    labels.append(Segment.getScore())
                    segment_ids.append(segment_id)

                    if Segment.Segment_OSM_MARKING_VERSION == OSM_MARKING_VERSION:
                        # only if we have one - checkOSMVersion could be used too

                        # Aaardwark, fix Segment.getNearbyVector(i_th_image) in Segment.LocationsIndex(i_th_image) -> Segment.LocationsIndex[i_th_image]
                        osm = Segment.DistinctNearbyVector[location_index]

                        osm_vectors.append(osm)

            #print len(list_of_images), len(labels), len(osm_vectors), len(segment_ids)

        segment_id += 1

    # If the path to images is specific, modify it from simple "Data/images/" with putting path_to_images before it.
    if (path_to_images is not None):
        # for example to ['images/000.jpg', ...] it will add "DifferentPath/" -> ['DifferentPath/images/000.jpg', ...]
        list_of_images = [(path_to_images+x) for x in list_of_images]


    # stats printing
    '''
    print 'number_no_score_yes_img', number_no_score_yes_img
    print 'number_no_score_no_img', number_no_score_no_img
    print 'number_yes_score_yes_img', number_yes_score_yes_img
    print 'number_yes_score_no_img', number_yes_score_no_img
    '''

    if len(osm_vectors) == 0:
        osm_vectors = [None] * len(list_of_images)

    return list_of_images, labels, osm_vectors, segment_ids, flag_is_extended

def LoadActualImages(list_of_images, resize=None, dim_ordering=KERAS_SETTING_DIMENSIONS):
    # Load actual image data from paths
    x = load_images_with_keras(list_of_images, target_size=resize, dim_ordering=dim_ordering)
    x = np.array(x)
    return x