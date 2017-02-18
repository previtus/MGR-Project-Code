from DataOperations import *
from KerasPreparation import *
from VisualizeHistory import *
from keras.utils.visualize_util import plot
import numpy as np

def TestModel(model, local_folder, path_to_images, output_model_img=True, output_history_plot=True):
    if output_model_img:
        plot(model, to_file=local_folder + 'results/model.png', show_shapes=True)

    # 1 load valid Segments
    Segments = LoadDataFile(path_to_images + 'SegmentsData.dump')
    UsableTrainSubset = SubsetSegments(Segments, has_image=True, has_score=True)

    # TODO> If we have labels_from_segments.npy + labels_from_model.npy load them, otherwise>
    '''
    # 3 labels_from_segments
    list_of_images, labels_from_segments = LoadDataFromSegments(UsableTrainSubset)
    if (path_to_images is not None):
        list_of_images = [(path_to_images + x) for x in list_of_images]


    # 4 labels_from_model
    img_width = 150
    img_height = 150
    validation_images = preprocess_image_batch(list_of_images, img_size=(PIXELS_X, PIXELS_Y), crop_size=(img_width, img_height), color_mode="rgb")

    labels_from_model = model.predict(validation_images, batch_size=32, verbose=0)

    # 5 COMPARE

    # numpy save and load:
    np.save(open(local_folder + 'data/labels_from_segments.npy', 'w'), labels_from_segments)
    np.save(open(local_folder + 'data/labels_from_model.npy', 'w'), labels_from_model)
    '''

    labels_from_segments = np.load(open(local_folder + 'data/labels_from_segments.npy'))
    labels_from_model = np.load(open(local_folder + 'data/labels_from_model.npy'))

    labels_from_model = labels_from_model[:,0]
    labels_from_segments  = np.float32(labels_from_segments )

    print "labels_from_segments: ", len_(labels_from_segments), map(type,labels_from_segments[0:1])
    print "labels_from_model: ", len_(labels_from_model), map(type,labels_from_model[0:1])

    from sklearn.metrics import *
    mse=mean_squared_error(labels_from_segments,labels_from_model)
    print "mean_absolute_error: ", mean_absolute_error(labels_from_segments,labels_from_model)
    print "mean_squared_error: ", mse
    print "root mean_squared_error: ", np.sqrt(mse)
    print "median_absolute_error: ", median_absolute_error(labels_from_segments,labels_from_model)
    print "R^2 (coefficient of determination)_score: ", r2_score(labels_from_segments,labels_from_model)

    # SSIM is useful when comparing two images (better then mse for edits of some pixels)
    from skimage.measure import compare_ssim
    print "ssim (+1 similar, -1 dissimilar): ", compare_ssim(labels_from_segments,labels_from_model)

    if output_history_plot:
        visualize_history(loadHistory(local_folder + 'results/history.npy'), show=False, save=True, save_path=local_folder + 'results/')

