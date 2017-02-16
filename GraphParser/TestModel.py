from DataOperations import *
from KerasPreparation import *
from keras.models import load_model

segments_filepath = '1200downloaded/SegmentsData.dump'
model_filepath = '1200downloaded/pokusCNN_s1000_e50.h5'
path_to_images = '1200downloaded/'

# 1 load valid Segments
Segments = LoadDataFile(segments_filepath, only_valid=True)

# 2 load model and validation data from files
model = load_model(model_filepath)

# 3 labels_from_segments
list_of_images, labels_from_segments = LoadDataFromSegments(Segments)
if (path_to_images is not None):
    list_of_images = [(path_to_images + x) for x in list_of_images]

'''
# 4 labels_from_model
img_width = 150
img_height = 150
validation_images = preprocess_image_batch(list_of_images, img_size=(PIXELS_X, PIXELS_Y), crop_size=(img_width, img_height), color_mode="rgb")

labels_from_model = model.predict(validation_images, batch_size=32, verbose=0)

# 5 COMPARE

# numpy save and load:
np.save(open('1200downloaded/labels_from_segments.npy', 'w'), labels_from_segments)
np.save(open('1200downloaded/labels_from_model.npy', 'w'), labels_from_model)
'''

labels_from_segments = np.load(open('1200downloaded/labels_from_segments.npy'))
labels_from_model = np.load(open('1200downloaded/labels_from_model.npy'))

labels_from_model = labels_from_model[:,0]
# coversion float64 > float32
labels_from_segments  = np.float32(labels_from_segments )

print "labels_from_segments: ", len_(labels_from_segments), map(type,labels_from_segments[0:1])
print "labels_from_model: ", len_(labels_from_model), map(type,labels_from_model[0:1])

#histogram_data = abs(labels_from_segments - labels_from_model)
#saveArrayToCSV(histogram_data,'abs_error.csv')

#mean_squared_error = ((labels_from_segments - labels_from_model) ** 2).mean(axis=0)
#root_mean_square_error = np.sqrt(((labels_from_segments - labels_from_model) ** 2).mean())
#max_abs_err = max(histogram_data)
#print max_abs_err
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
