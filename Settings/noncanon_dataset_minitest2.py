def Setup(Settings,DefaultModel):
    # noncanon_dataset_minitest2.py


    Settings["experiment_name"] = "NonCanonDataset"

    Settings["graph_histories"] = ['together']

    n=0
    Settings["models"][n]["noncanon_dataset"] = 'expand_existing_dataset'

    from keras.preprocessing.image import ImageDataGenerator
    from DatasetHandler.custom_image import ImageDataGenerator as custom_ImageDataGenerator

    image_generator = custom_ImageDataGenerator(
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

    defaults = custom_ImageDataGenerator(
        featurewise_center=False, # Set input mean to 0 over the dataset, feature-wise.
        samplewise_center=False, # Set each sample mean to 0.
        featurewise_std_normalization=False, # Divide inputs by std of the dataset, feature-wise.
        samplewise_std_normalization=False, # Divide each input by its std.
        zca_whitening=False, # Apply ZCA whitening.
        rotation_range=0., # Degree range for random rotations.
        width_shift_range=0., # Range for random horizontal shifts (fraction of total width).
        height_shift_range=0., # Range for random vertical shifts (fraction of total height).
        shear_range=0., # Shear Intensity (Shear angle in counter-clockwise direction as radians)
        zoom_range=0., # Float or [lower, upper]. Range for random zoom. If a float, [lower, upper] = [1-zoom_range, 1+zoom_range].
        channel_shift_range=0., # Range for random channel shifts.
        fill_mode='nearest', # One of {"constant", "nearest", "reflect" or "wrap"}. Points outside the boundaries of the input are filled according to the given mode.
        cval=0., # Float or Int. Value used for points outside the boundaries when fill_mode = "constant".
        horizontal_flip=False, # Randomly flip inputs horizontally.
        vertical_flip=False, # Randomly flip inputs vertically.
        rescale=None, # rescaling factor. Defaults to None. If None or 0, no rescaling is applied, otherwise we multiply the data by the value provided (before applying any other transformation).
        preprocessing_function=None,
        # function that will be implied on each input. The function will run before any other modification on it.
        # The function should take one argument: one image (Numpy tensor with rank 3), and should output a Numpy tensor with the same shape.
    )

    Settings["models"][n]["noncanon_dataset_imagegenerator"] = image_generator
    Settings["models"][n]["noncanon_dataset_genfrom1"] = 3

    Settings["models"][n]["model_type"] = 'simple_cnn_with_top'
    Settings["models"][n]["dataset_name"] = "miniset_640px_expanded"
    Settings["models"][n]["pixels"] = 640
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'testingExpanding'
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = 5
    #Settings["models"][n]["dump_file_override"] = 'SegmentsData_marked_R100_4Tables.dump'
    Settings["models"][n]["extended_dir_name"] = 'images_generated_test_folder'
    Settings["models"][n]["dump_file_expanded"] = 'SegmentsData_' + Settings["models"][n]["extended_dir_name"] + '_expanded.dump'

    return Settings
