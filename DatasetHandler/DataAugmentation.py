from Omnipresent import len_
import os
from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist

def handle_noncanon_dataset(Settings, model_settings):
    '''
    We are creating a new custom dataset, instead of using one of the big officially used, "canon" datasets
    :param Settings: Setting for the whole experiment
    :param model_settings: Setting for our one dataset
    :return:
    '''
    dataset = None

    if model_settings["noncanon_dataset"] == 'expand_existing_dataset':
        # Idea: take an existing dataset and expand it via

        # Directly load the old segments file

        # for each segment
        #   for each image
        #       apply the custom ImageDataGenerator to generate new images (depending of settings)
        #       save the new images into target folder as well as into this Segment
        # save edited Segments array into new SegmentsFile.dump

        debug_visual_output = True

        from DatasetHandler.CreateDataset import get_path_for_dataset
        from Downloader.DataOperations import LoadDataFile
        from Downloader.KerasPreparation import LoadActualImages
        import numpy as np

        if debug_visual_output:
            from matplotlib import pyplot
            from keras.preprocessing.image import array_to_img
            import math

        folder = model_settings["dataset_name"]
        filename_override = model_settings["dump_file_override"]
        segments_path = get_path_for_dataset(folder, filename_override)
        segments_dir = os.path.dirname(segments_path) + '/'

        generated_images_folder = os.path.dirname(segments_path) + '/images_generated/'
        print 'generated_images_folder', generated_images_folder
        make_folder_ifItDoesntExist(generated_images_folder)


        print segments_path  # /home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_minlen30_640px/SegmentsData.dump
        print segments_dir   # /home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_minlen30_640px/

        size_of_batch = model_settings["noncanon_dataset_genfrom1"]

        image_generator = model_settings["noncanon_dataset_imagegenerator"]
        print "image_generator", image_generator
        #image_generator.fit(X_train)

        Segments = LoadDataFile(segments_path)

        number_of_images_parsed = 0
        for Segment in Segments:
            for i_th_image in range(0,Segment.number_of_images):
                if Segment.hasLoadedImageI(i_th_image):
                    filename = segments_dir+Segment.getImageFilename(i_th_image)
                    number_of_images_parsed += 1
                    print filename

                    # we have one image filepath - generate data
                    x = LoadActualImages([filename])
                    y = np.array([Segment.SegmentId])
                    print "ORIGINAL id", y, "img:", len_(x[0])

                    X_batch = []
                    y_batch = []

                    from DatasetHandler.custom_image import ImageDataGenerator as custom_ImageDataGenerator
                    number_of_images_generated = 0
                    for x_gen, y_gen in image_generator.flow(x, y, batch_size=1, save_to_dir=generated_images_folder, save_prefix=str(y)+'_', save_format='jpg'):
                        number_of_images_generated += 1
                        image = x_gen[0]

                        filename_generated = y_gen[1][0]
                        id = y_gen[0][0]

                        print id, filename_generated

                        # save image on path filename_generated to the Segments hierarchy!
                        print "Segment.number_of_images", Segment.number_of_images
                        print "Segment.LocationsIndex", Segment.LocationsIndex
                        print "Segment.DistinctLocations", Segment.DistinctLocations
                        print "Segment.DistinctNearbyVector", Segment.DistinctNearbyVector
                        print "Segment.HasLoadedImages", Segment.HasLoadedImages
                        print "Segment.ErrorMessages", Segment.ErrorMessages

                        new_filename_generated = Segment.getImageFilename(Segment.number_of_images+number_of_images_generated)
                        print "rename", filename_generated, "to", new_filename_generated

                        print "---"

                        X_batch.append(image)
                        y_batch.append(id)

                        #print "id", y_gen, "img:", len_(x_gen), array_md5(image)

                        if len(X_batch) == size_of_batch:

                            print "GENERATED ", len(y_batch), " images > ", len_(X_batch), y_batch

                            if debug_visual_output:
                                # create a grid of 3x3 images
                                size_for_plot = int(math.floor(math.sqrt(size_of_batch-0.1))+1)
                                size_for_plot_y = size_for_plot
                                while size_of_batch <= size_for_plot*(size_for_plot_y-1):
                                    size_for_plot_y -= 1

                                print size_for_plot, "x", size_for_plot_y, " grid"

                                for i in range(0, len(X_batch)):
                                    pyplot.subplot(size_for_plot_y,size_for_plot,i+1)

                                    img = X_batch[i]
                                    backimg = array_to_img(img)
                                    pyplot.imshow(backimg)
                                # show the plot
                                pyplot.show()
                                break

                            break # end generation for this one image
                    print "Save new images from id", y, " in", len_(X_batch)
        print "number_of_images_parsed", number_of_images_parsed


        #Segments = DataOperations.LoadDataFile(path_to_segments_file)
        #segments_dir = os.path.dirname(path_to_segments_file) + '/'

        '''
        # make this into function i guess
        path_r100 = ABS_PATH_TO_PRJ+'Data/StreetViewData/'+folder+'/SegmentsData_marked_R100.dump'
        path = ABS_PATH_TO_PRJ+'Data/StreetViewData/'+folder+'/SegmentsData.dump'

        path_override = ABS_PATH_TO_PRJ+'Data/StreetViewData/'+folder+'/' + filename_override

        if os.path.isfile(path_r100):
            path = path_r100

        if filename_override <> '' and os.path.isfile(path_override):
            path = path_override
        '''




        '''
        dataset = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
            desired_number=model_settings["number_of_images"], seed=model_settings["seed"], filename_override=model_settings["dump_file_override"])

        xy_generator = dataset.generator_of_all_data()
        for X_batch, y_batch in xy_generator:
            #print y_batch
            print len_(X_batch), len_(y_batch), y_batch
        '''

        # we need a generator over existing dataset, which will get
        # X, y - where X are images and y the rest of data

        # create new dump file out of these ... ouch

        # datagen = ImageDataGenerator(...) load that one from Setting, should have unique name

        # flow(X, y) where X are images and in y everything else needed to make one data unit for dataset
        '''
        datagen = ImageDataGenerator()
        imdgen = ImageDataGenerator(
            featurewise_center = False,  # set input mean to 0 over the dataset
            samplewise_center = False,  # set each sample mean to 0
            featurewise_std_normalization = False,  # divide inputs by std of the dataset
            samplewise_std_normalization = False,  # divide each input by its std
            zca_whitening = False,  # apply ZCA whitening
            rotation_range = 0,  # randomly rotate images in the range (degrees, 0 to 180)
            width_shift_range = 0.1,  # randomly shift images horizontally (fraction of total width)
            height_shift_range = 0.1,  # randomly shift images vertically (fraction of total height)
            horizontal_flip = True,  # randomly flip images
            vertical_flip = False,  # randomly flip images
        )
        for X_batch, y_batch in datagen.flow(X_train, y_train, batch_size=9, save_to_dir='images', save_prefix='aug', save_format='png'):
        '''
    else:
        print "This type of noncanon dataset generation has not yet been implemented!"

    return dataset
