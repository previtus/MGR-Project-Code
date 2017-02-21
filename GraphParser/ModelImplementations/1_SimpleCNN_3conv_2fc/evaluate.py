from keras.models import load_model
from Tester import TestModel

PathToImages = '../../1100downloaded_vII/'
LocalFolder = ''

model = load_model(LocalFolder+'data/pokusCNN_V2_s1000_e5.h5')
TestModel(model, LocalFolder, PathToImages, output_model_img=True, output_history_plot=True)