def Setup(Settings,DefaultModel):
    # set7_dataset-aggressive-expansion/aggresive_expand_dataset_minlen30_kfold.py


    Settings["experiment_name"] = "aggresive_expand_dataset_minlen30_kfold"

    Settings["graph_histories"] = ['together']

    n=0

    from keras.preprocessing.image import ImageDataGenerator
    from DatasetHandler.custom_image import ImageDataGenerator as custom_ImageDataGenerator

    image_generator = custom_ImageDataGenerator(
            featurewise_center = False,  # set input mean to 0 over the dataset
            samplewise_center = False,  # set each sample mean to 0
            featurewise_std_normalization = False,  # divide inputs by std of the dataset
            samplewise_std_normalization = False,  # divide each input by its std
            zca_whitening = False,  # apply ZCA whitening
            rotation_range = 10.0,  # randomly rotate images in the range (degrees, 0 to 180)
            width_shift_range = 0.2,  # randomly shift images horizontally (fraction of total width)
            height_shift_range = 0.2,  # randomly shift images vertically (fraction of total height)
            horizontal_flip = True,  # randomly flip images
            vertical_flip = False,  # randomly flip images
            shear_range=0.2,
            zoom_range=0.2,
    )

    # Set these values:
    number_of_images_from_one = 2
    source_dataset = "5556x_minlen30_640px"
    target_dataset = "5556x_minlen30_640px_2x_agressive_expanded"
    pixels = 640
    epochs = 500
    use_dump_file = 'SegmentsData_marked_R100_4Tables.dump' # -> * new XYZ_expanded.dump

    model_type = 'img_osm_mix'

    # Feed the monkey and don't touch anything!
    Settings["models"][n]["noncanon_dataset"] = 'expand_existing_dataset'
    Settings["models"][n]["noncanon_dataset_imagegenerator"] = image_generator
    Settings["models"][n]["noncanon_dataset_genfrom1"] = number_of_images_from_one

    Settings["models"][n]["model_type"] = model_type
    Settings["models"][n]["dataset_name"] = target_dataset
    Settings["models"][n]["source_dataset"] = source_dataset
    Settings["models"][n]["pixels"] = pixels
    Settings["models"][n]["cnn_model"] = 'resnet50'
    Settings["models"][n]["unique_id"] = 'expanded: ' + target_dataset
    Settings["models"][n]["cooking_method"] = 'generators' # 'direct' or 'generators'
    Settings["models"][n]["epochs"] = epochs

    Settings["models"][n]["dump_file_override"] = use_dump_file
    Settings["models"][n]["dump_file_expanded"] = use_dump_file[:-5] + '_expanded.dump'

    Settings["models"][n]["k_fold_crossvalidation"] = True
    Settings["models"][n]["crossvalidation_k"] = 10

    Settings["graph_histories"] = []

    return Settings
