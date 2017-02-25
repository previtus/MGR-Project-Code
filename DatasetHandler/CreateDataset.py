from DatasetObj import Dataset
import time
from Downloader.ImageHelpers import len_
import numpy as np

#path = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/Data/StreetViewData/TestData/SegmentsData.dump'
#path = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/Downloader/SegmentsData.dump'
path = '../Data/StreetViewData/8376_valid_images_640x640_120deg_turns_from_all_segments/SegmentsData.dump'
testDataset = Dataset()
testDataset.init_from_segments(path, 640, 640)
testDataset.statistics()
#testDataset.plotHistogram(save_to_pdf=True)

n = 100
[list_of_images, labels] = testDataset.DebugGetDatasetArrays()
#list_of_images = list_of_images[0:n]
#labels = labels[0:n]

testDataset_smaller = testDataset.spawnUniformSubset(1000)
testDataset_smaller.plotHistogram()


#import matplotlib.pyplot as plt
#plt.plot(indices)

'''
count, bins, ignored = plt.hist(indices, 1000, normed=True)
plt.plot(bins, np.ones_like(bins), linewidth=2, color='r')
'''

#plt.show()

#img_size=(299, 299)
#[x, y, x_val, y_val] = testDataset.getDataLabels_split(resize=img_size)
#start = time.time()
#[x, y, x_val, y_val] = testDataset.getDataLabels_split()
#end = time.time()
#print "Took", (end - start), "sec to load."
#print len_(x)
#print len_(y)
#print len_(x_val)
#print len_(y_val)
