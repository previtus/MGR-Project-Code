from Omnipresent import len_
import os
import shutil
from DatasetHandler.FileHelperFunc import use_path_which_exists, make_folder_ifItDoesntExist, copy_folder, file_exists, folder_exists

def handle_noncanon_dataset(Settings, model_settings):
    '''
    We are creating a new custom dataset, instead of using one of the big officially used, "canon" datasets
    :param Settings: Setting for the whole experiment
    :param model_settings: Setting for our one dataset
    :return:
    '''

    if model_settings["noncanon_dataset"] == 'expand_existing_dataset':
        # Idea: take an existing dataset and expand it via

        # Directly load the old segments file

        # for each segment
        #   for each image
        #       apply the custom ImageDataGenerator to generate new images (depending of settings)
        #       save the new images into target folder as well as into this Segment
        # save edited Segments array into new SegmentsFile.dump

        debug_visual_output = False
        debug_txt_output = False

        from DatasetHandler.CreateDataset import get_path_for_dataset
        from Downloader.DataOperations import LoadDataFile
        from Downloader.KerasPreparation import LoadActualImages
        import numpy as np

        if debug_visual_output:
            from matplotlib import pyplot
            from keras.preprocessing.image import array_to_img
            import math

        target_folder = model_settings["dataset_name"]
        source_folder = model_settings["source_dataset"]

        filename_override = model_settings["dump_file_override"]
        source_segments_path = get_path_for_dataset(source_folder, filename_override)
        source_segments_dir = os.path.dirname(source_segments_path) + '/'

        if not file_exists(source_segments_dir + filename_override):
            print "WARNING !!!!"
            print '\t',"Careful, couldn't find the file", source_segments_dir + filename_override
            print '\t',"... we will instead be using   ", source_segments_path


        target_segments_path = get_path_for_dataset(target_folder, '')
        target_segments_dir = os.path.dirname(target_segments_path) + '/'
        target_segments_path = target_segments_dir+model_settings["dump_file_expanded"]

        # Check if we don't alredy have it?
        if (file_exists(target_segments_path) and folder_exists(target_segments_dir+'images') and folder_exists(target_segments_dir+'images_extended')):
            list1 = os.listdir(target_segments_dir+'images')
            list2 = os.listdir(source_segments_dir+'images')
            if len(list1)==len(list2):
                # Seems like we have copied it correctly too

                print "We already have this dataset extended! (", len(list1), len(list2), ")"

                return
        else:
            print '\t', file_exists(target_segments_path), target_segments_path
            print '\t', folder_exists(target_segments_dir+'images'), target_segments_dir+'images'
            print '\t', folder_exists(target_segments_dir+'images_extended'), target_segments_dir+'images_extended'


        generated_images_folder = os.path.dirname(target_segments_path) + '/images_extended/'
        print 'generated_images_folder', generated_images_folder
        make_folder_ifItDoesntExist(generated_images_folder)

        print "source_segments_path", source_segments_path  # /home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/miniset_640px/SegmentsData.dump
        print "source_segments_dir", source_segments_dir    # /home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/miniset_640px/
        print "target_segments_path", target_segments_path  # /home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/miniset_640px_expanded/SegmentsData_images_generated_test_folder_expanded.dump
        print "target_segments_dir", target_segments_dir    # /home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/miniset_640px_expanded/

        # copy source_dataset -> target_dataset in dataset_name
        # from source_segments_dir/images to  target_segments_dir/images
        copy_folder(source_segments_dir+'images', target_segments_dir+'images')

        size_of_batch = model_settings["noncanon_dataset_genfrom1"]

        image_generator = model_settings["noncanon_dataset_imagegenerator"]
        print "image_generator", image_generator
        #image_generator.fit(X_train)

        Segments = LoadDataFile(source_segments_path)

        number_of_images_parsed = 0
        for Segment in Segments:
            number_of_images = Segment.number_of_images
            for i_th_image in range(0,number_of_images):
                if Segment.hasLoadedImageI(i_th_image):
                    filename = source_segments_dir+Segment.getImageFilename(i_th_image)
                    number_of_images_parsed += 1
                    print filename

                    # we have one image filepath - generate data
                    x = LoadActualImages([filename])
                    y = np.array([Segment.SegmentId])
                    if debug_txt_output:
                        print "ORIGINAL id", y, "ith", i_th_image, "img:", len_(x[0])

                    X_batch = []
                    y_batch = []

                    from DatasetHandler.custom_image import ImageDataGenerator as custom_ImageDataGenerator
                    number_of_images_generated = 0
                    for x_gen, y_gen in image_generator.flow(x, y, batch_size=1, save_to_dir=generated_images_folder, save_prefix=str(y)+'_', save_format='jpg'):
                        number_of_images_generated += 1
                        image = x_gen[0]

                        filename_generated = y_gen[1][0]
                        id = y_gen[0][0]

                        if debug_txt_output:
                            print id, filename_generated

                            # save image on path filename_generated to the Segments hierarchy!
                            print "Segment.number_of_images", Segment.number_of_images
                            print "Segment.LocationsIndex", Segment.LocationsIndex
                            print "Segment.DistinctLocations", Segment.DistinctLocations
                            print "Segment.DistinctNearbyVector", Segment.DistinctNearbyVector
                            print "Segment.HasLoadedImages", Segment.HasLoadedImages
                            print "Segment.ErrorMessages", Segment.ErrorMessages

                        # Value 200 is the marker
                        location_index = Segment.LocationsIndex[i_th_image] + 200
                        # accordingly we get Segment.DistinctLocations[location_index] and Segment.DistinctNearbyVector[location_index]
                        has_img = Segment.HasLoadedImages[i_th_image]
                        has_err = Segment.ErrorMessages[i_th_image]

                        # Add to this Segment
                        Segment.number_of_images += 1
                        Segment.LocationsIndex.append(location_index)
                        Segment.HasLoadedImages.append(has_img)
                        Segment.ErrorMessages.append(has_err)


                        # Change filename and path
                        new_filename_generated = target_segments_dir + 'images_extended' + Segment.getImageFilename(Segment.number_of_images-1)[6:]
                        if debug_txt_output:
                            print "rename", filename_generated, "to", new_filename_generated

                        shutil.move(filename_generated, new_filename_generated)

                        print ".", new_filename_generated

                        X_batch.append(image)
                        y_batch.append(id)

                        #print "id", y_gen, "img:", len_(x_gen), array_md5(image)

                        if len(X_batch) == size_of_batch:

                            if debug_txt_output:
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
                    if debug_txt_output:
                        print "Save new images from id", y, " in", len_(X_batch)
        print "number_of_images_parsed", number_of_images_parsed


        from Downloader.DataOperations import SaveDataFile
        print "Saving new Segments file into ", target_segments_path
        SaveDataFile(target_segments_path, Segments)

    else:
        print "This type of noncanon dataset generation has not yet been implemented!"

