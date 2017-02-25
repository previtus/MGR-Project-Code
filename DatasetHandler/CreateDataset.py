from DatasetObj import Dataset
import time
from Downloader.ImageHelpers import len_

start = time.time()

#path = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/Data/StreetViewData/TestData/SegmentsData.dump'
#path = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/Downloader/SegmentsData.dump'
path = '../Data/StreetViewData/8376_valid_images_640x640_120deg_turns_from_all_segments/SegmentsData.dump'
testDataset = Dataset()
testDataset.init_from_segments(path, 640, 640)
testDataset.statistics()
#testDataset.plotHistogram(save_to_pdf=True)



#img_size=(299, 299)
#[x, y, x_val, y_val] = testDataset.getDataLabels_split(resize=img_size)

#[x, y, x_val, y_val] = testDataset.getDataLabels_split()

end = time.time()
print "Took", (end - start), "sec to load."

#print len_(x)
#print len_(y)
#print len_(x_val)
#print len_(y_val)
