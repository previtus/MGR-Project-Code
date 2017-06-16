from ImageHelpers import *
from keras.preprocessing.image import ImageDataGenerator

from Defaults import *
from DataOperations import *
from PreprocessData.SegmentsManipulators import *

def split_one_array(arr,validation_split=0.2):
    if not(0 < validation_split < 1):
        print "Choose validation_split in between 0 and 1. Setting the default value of 0.2"
        validation_split = 0.2

    split_at = int(len(arr) * (1 - validation_split))
    arr_test = arr[0:split_at]
    arr_val = arr[split_at:]
    return arr_test,arr_val

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
    if not(0 < validation_split < 1):
        print "Choose validation_split in between 0 and 1. Setting the default value of 0.2"
        validation_split = 0.2

    split_at = int(len(osm) * (1 - validation_split))
    osm_test = osm[0:split_at]
    osm_val = osm[split_at:]
    return osm_test, osm_val

def LoadDataFromSegments(Segments, has_score=True, path_to_images=None):
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
                if location_index > 100:
                    # then this particular image is loaded from an extended folder
                    is_extended = True
                    location_index -= 200
                    flag_is_extended = True
                if Segment.hasLoadedImageI(i_th_image):

                    filename = Segment.getImageFilename(i_th_image)
                    if is_extended:
                        filename = 'images_generated_test_folder' + filename[6:]
                    list_of_images.append(filename)
                    labels.append(Segment.getScore())
                    segment_ids.append(segment_id)

                if Segment.Segment_OSM_MARKING_VERSION == OSM_MARKING_VERSION:
                    # only if we have one - checkOSMVersion could be used too

                    # Aaardwark, fix Segment.getNearbyVector(i_th_image) in Segment.LocationsIndex(i_th_image) -> Segment.LocationsIndex[i_th_image]
                    osm = Segment.DistinctNearbyVector[location_index]

                    osm_vectors.append(osm)

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
    x = load_images_with_keras(list_of_images, target_size=resize, dim_ordering=dim_ordering)

    #x = preprocess_image_batch(list_of_images, img_size=resize)

    x = np.array(x)
    return x


#### NOT USED

def Prepare_DataLabels_nosplit(Segments, img_width, img_height, path_to_images=None):

    # Open Segments and check images and scores
    if (PIXELS_X != img_width) or (PIXELS_Y != img_height):
        print "Downloaded images are of (PIXELS_X, PIXELS_Y):",PIXELS_X, PIXELS_Y, ", while we want (img_width, img_height)", img_width, img_height

    StatisticsSegments(Segments)
    list_of_images, y, _ = LoadDataFromSegments(Segments, has_score=True, path_to_images=path_to_images)

    # TODO: figure out a way of seleting correct sizes. Ideally we want to download biggest images possible and them crop bits out of them.
    x = preprocess_image_batch(list_of_images, img_size=(PIXELS_X, PIXELS_Y), crop_size=(img_width, img_height))
    n = len(list_of_images)
    return [x, y, n]

def Prepare_DataLabels(Segments, img_width, img_height,validation_split=0.2, path_to_images=None):
    '''
    Prepares data for Keras into inputs in x (images which will be fed into CNN) and their particular labels in y
    (labels which will be compared with outputs on CNN later). Also produces validation set.

    :param path_to_segments_file: Path to where segments are saved (usually in Defaults.py)
    :param img_width: wanted outputing resolution (no matter how we saved the actual data)
    :param img_height:
    :param validation_split:
    :param path_to_images: additional path specification which we need before 'images/---.jpg'
    :return: Returns the data suitable for Keras - in x sized by (num_of_data,3,w,h) and in y sized by (num_of_data)
    '''
    [x, y, n] = Prepare_DataLabels_nosplit(Segments, img_width, img_height, path_to_images=path_to_images)
    x, y, x_val, y_val = split_data(x, y, validation_split)

    print "Valid segments ",n,". Prepared dataset of", len(x) ,"train and", len(x_val), "validation images of size",img_width,"x",img_height,"."
    return [x, y, x_val, y_val]

def Prepare_DataLabels_generators(Segments, img_width, img_height,validation_split=0.2, path_to_images=None,
    valid_datagen_overwrite=None, train_datagen_overwrite=None, shuffle_=True, batch_size_=32):
    '''
    Prepares generators of data for Keras in training and validation set.

    Example of usage of the generators:
     model.fit_generator( train_generator, samples_per_epoch=<number of training samples>, nb_epoch=<number of epochs>,
        validation_data=validation_generator, nb_val_samples=<number of validation samples>, callbacks=[])

    '''

    # Get full sized images
    [x, y, x_val, y_val] = Prepare_DataLabels(Segments, img_width, img_height,validation_split, path_to_images)

    if (valid_datagen_overwrite is None):
        valid_datagen = ImageDataGenerator(rescale=1. / 255)
    else:
        valid_datagen = valid_datagen_overwrite

    if (train_datagen_overwrite is None):
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
    else:
        train_datagen = train_datagen_overwrite

    train_generator = train_datagen.flow(
        x, y,
        batch_size=batch_size_,
        shuffle=shuffle_
    )

    validation_generator = valid_datagen.flow(
        x_val, y_val,
        batch_size=batch_size_,
        shuffle=shuffle_
    )

    return [train_generator, validation_generator]

def GenerateData(x,y, ImgDataGenerator, target_number_of_images,shuffle_=True, seed_=None):
    '''
    From already loaded dataset of images and their labels generates dataset of given size using ImgDataGenerator

    :param x: images
    :param y: their labels
    :param ImgDataGenerator: Keras ImageDataGenerator object
    :param target_number_of_images: how many resulting images we want
    :return: the new dataset
    '''

    generator_flow = ImgDataGenerator.flow(
        x, y,
        batch_size=1,
        shuffle=shuffle_,
        seed=seed_
        # DEBUG purposes> #save_to_dir='1100downloaded_vII/preview', save_prefix='cat', save_format='jpeg'
    )

    x_gen = []
    y_gen = []
    i = 0

    for batch in generator_flow:
        i += 1
        img = batch[0][0]
        label = batch[1]
        x_gen.append(img)
        y_gen.append(label)

        #print len_(img), label
        if i >= target_number_of_images:
            break

    x_gen = np.array(x_gen)
    return [x_gen,y_gen]

def Prepare_DataLabels_withGeneratedData(Segments, img_width, img_height,validation_split=0.2,
      path_to_images=None, valid_datagen_overwrite=None, train_datagen_overwrite=None, target_number_of_trainset = 2000, target_number_of_validset = None,
                                         shuffle_=True, seed_=None):
    '''
    From existing dataset of images in Semgent data creates training and validation subsets (in ratio validation_split)
    then uses Keras ImageDataGenerator to generate altered images of the given amount (target_number_of_trainset and target_number_of_validset)

    Example of usage of the generators:
        [x_gen, y_gen, x_val_gen, y_val_gen] = Prepare_DataLabels_withGeneratedData(DATASTRUCTUREFILE,150,150)
        fit( ... )
             ... is similar to: x_gen, y_gen, validation_data=(x_val_gen, y_val_gen as tuple)

    :param path_to_segments_file: Path to where segments are saved (usually in Defaults.py)
    :param img_width: wanted outputing resolution (no matter how we saved the actual data)
    :param img_height:
    :param validation_split:
    :param path_to_images: additional path specification which we need before 'Data/images/---.jpg'
    :param valid_datagen_overwrite: Custom ImageDataGenerator object for validation data
    :param train_datagen_overwrite: Custom ImageDataGenerator object for training data
    :param target_number_of_trainset: Size of the training set we want
    :param target_number_of_validset: If left to None, defaults to (target_number_of_trainset*validation_split)
    :return:
    '''

    if (target_number_of_validset is None):
        target_number_of_validset = target_number_of_trainset*validation_split

    # Get full sized images
    [x, y, x_val, y_val] = Prepare_DataLabels(Segments, img_width, img_height, validation_split,
                                              path_to_images)

    if (valid_datagen_overwrite is None):
        valid_datagen = ImageDataGenerator(rescale=1. / 255)
    else:
        valid_datagen = valid_datagen_overwrite

    if (train_datagen_overwrite is None):
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True
        )
    else:
        train_datagen = train_datagen_overwrite

    [x_gen, y_gen] = GenerateData(x, y, train_datagen, target_number_of_trainset, shuffle_=shuffle_, seed_=seed_)
    [x_val_gen, y_val_gen] = GenerateData(x_val, y_val, valid_datagen, target_number_of_validset, shuffle_=shuffle_, seed_=seed_)

    print "Generated dataset of", len(x_gen) ,"train and", len(x_val_gen), "validation images of size",img_width,"x",img_height,"."
    return [x_gen, y_gen, x_val_gen, y_val_gen]

#Folder = '1100downloaded_vII/'
#[x, y, x_val, y_val] = Prepare_DataLabels(Folder+DATASTRUCTUREFILE,150,150,path_to_images=Folder)
#[train_generator, validation_generator] = Prepare_DataLabels_generators(Folder+DATASTRUCTUREFILE,150,150)
#Prepare_DataLabels_withGeneratedData(Folder+DATASTRUCTUREFILE,150,150,path_to_images=Folder)

#train_generator = ImageDataGenerator(rescale=1. / 255)
#[x_gen, y_gen] = GenerateData(x, y, train_generator, 5)
'''
print x_gen
print y_gen
print type(x_gen)
print type(y_gen)
'''
