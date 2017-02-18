from ImageHelpers import *
from keras.preprocessing.image import ImageDataGenerator

from Defaults import *
from DataOperations import *
from PreprocessData.SegmentsManipulators import *

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

def LoadDataFromSegments(Segments):
    '''
    Turns loaded segments into data we will need for keras.
    :param Segments: Loaded segments
    :return: Returns list of urls of images and their labels (score in the Segment)
    '''
    list_of_images = []
    labels = []

    for Segment in Segments:
        # We disregard those with no image or with score -1 (unknown attractivity)
        if Segment.isValidSegment():
            list_of_images.append(Segment.getImageFilename())
            labels.append(Segment.getScore())

    return list_of_images, labels

def Prepare_DataLabels(path_to_segments_file, img_width, img_height,validation_split=0.2, path_to_images=None):
    '''
    Prepares data for Keras into inputs in x (images which will be fed into CNN) and their particular labels in y
    (labels which will be compared with outputs on CNN later). Also produces validation set.

    :param path_to_segments_file: Path to where segments are saved (usually in Defaults.py)
    :param img_width: wanted outputing resolution (no matter how we saved the actual data)
    :param img_height:
    :param validation_split:
    :param path_to_images: additional path specification which we need before 'Data/images/---.jpg'
    :return: Returns the data suitable for Keras - in x sized by (num_of_data,3,w,h) and in y sized by (num_of_data)
    '''


    # Open Segments and check images and scores
    if (PIXELS_X != img_width) or (PIXELS_Y != img_height):
        print "Downloaded images are of (PIXELS_X, PIXELS_Y):",PIXELS_X, PIXELS_Y, ", while we want (img_width, img_height)", img_width, img_height

    Segments = LoadDataFile(path_to_segments_file)
    StatisticsSegments(Segments)
    UsableTrainSubset = SubsetSegments(Segments, has_image=True, has_score=True)
    list_of_images, labels = LoadDataFromSegments(UsableTrainSubset)

    # If the path to images is specific, modify it from simple "Data/images/" with putting path_to_images before it.
    if (path_to_images is not None):
        # for example to ['Data/images/000.jpg', ...] it will add "DifferentPath/" -> ['DifferentPath/Data/images/000.jpg', ...]
        list_of_images = [(path_to_images+x) for x in list_of_images]

    # TODO: figure out a way of seleting correct sizes. Ideally we want to download biggest images possible and them crop bits out of them.
    x = preprocess_image_batch(list_of_images, img_size=(PIXELS_X, PIXELS_Y), crop_size=(img_width, img_height), color_mode="rgb")
    x, y, x_val, y_val = split_data(x, labels, validation_split)

    print "Valid segments ",len(list_of_images),". Prepared dataset of", len(x) ,"train and", len(x_val), "validation images of size",img_width,"x",img_height,"."
    return [x, y, x_val, y_val]

def Prepare_DataLabels_generators(path_to_segments_file, img_width, img_height,validation_split=0.2, path_to_images=None, valid_datagen_overwrite=None, train_datagen_overwrite=None):
    '''
    Prepares generators of data for Keras in training and validation set.

    Example of usage of the generators:
     model.fit_generator( train_generator, samples_per_epoch=<number of training samples>, nb_epoch=<number of epochs>,
        validation_data=validation_generator, nb_val_samples=<number of validation samples>, callbacks=[])

    '''

    # Get full sized images
    [x, y, x_val, y_val] = Prepare_DataLabels(path_to_segments_file, img_width, img_height,validation_split, path_to_images)

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
        batch_size=32,
    )

    validation_generator = valid_datagen.flow(
        x_val, y_val,
        batch_size=32,
    )

    return [train_generator, validation_generator]


#[x, y, x_val, y_val] = Prepare_DataLabels(DATASTRUCTUREFILE,300,300,path_to_images=None)
#[train_generator, validation_generator] = Prepare_DataLabels_generators(DATASTRUCTUREFILE,222,222)