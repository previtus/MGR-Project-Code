from keras.models import load_model
from Tester import TestModel

from load_vgg16_model_with_top import load_vgg16_model_with_custom_top

PathToImages = '../../1100downloaded_vII/'
LocalFolder = ''

path_to_custom_top = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/Downloader/ModelImplementations/2_VGG16_no_finetuning/now1/data/top_model_weights.h5'
model = load_vgg16_model_with_custom_top(path_to_custom_top)

print "Loaded now testing."
TestModel(model, LocalFolder, PathToImages, bake_files=False)
