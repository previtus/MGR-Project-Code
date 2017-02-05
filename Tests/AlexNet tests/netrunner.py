PATH_TO_CONVNETS_KERAS = '/home/ekmek/TEMP_SPACE/convnets-keras/' #not pretty
import sys
sys.path.insert(0, PATH_TO_CONVNETS_KERAS)
from convnetskeras.convnets import convnet

def netrunner():
	"""
	Provides the handle on a model from https://github.com/heuritech/convnets-keras
	"""

	from keras.optimizers import SGD

	sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
	model = convnet('alexnet',weights_path="".join([PATH_TO_CONVNETS_KERAS, "weights/alexnet_weights.h5"]), heatmap=False)
	model.compile(optimizer=sgd, loss='mse')

	"""
	call with:
	im = preprocess_image_batch(['examples/cheetah1.jpg'],img_size=(256,256), crop_size=(227,227), color_mode="rgb")
	out = model.predict(im)
	"""

	return model

# print netrunner()