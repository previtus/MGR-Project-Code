PATH_TO_CONVNETS_KERAS = '/home/ekmek/TEMP_SPACE/convnets-keras/' #not pretty
import sys
sys.path.insert(0, PATH_TO_CONVNETS_KERAS)
from convnetskeras.convnets import preprocess_image_batch

def classification( image_list, output_file, topN, model_handler ):
	"""
	Runs classification on a set of images given by <image_list>.
	Gets <categories_topNerror> suggestions for each.
	Saves the result into <output_file> with following structure:
	   each line: image_name, classes (1 to <topN>)
	
	"""
	classifications = []
	
	for img_path in image_list:
		#print img_path
		# in the original form the image file is named for example:
		# 	ILSVRC2010_val_00000009.JPEG
		# subset -13, -5
		# print img_path[-13:-5] # 00000605 -> 605
		image_number = int(img_path[-13:-5])
		
		# prepare image
		im = preprocess_image_batch([img_path],img_size=(256,256), crop_size=(227,227), color_mode="rgb")

		# use model
		out = model_handler.predict(im)
		values = out[0]

		from convnetskeras.imagenet_tool import id_to_synset
		import numpy as np
		indices = np.argpartition(values, -topN)[-topN:]
		indices = indices[np.argsort(-values[indices])]

		# we quite dont need the probabilities
		#probabilities = values[indices]
		probabilities = []

		#print indices
		#print probabilities

		#classifications.append([image_number, indices.tolist(), probabilities.tolist()])
		classifications.append([image_number, indices, probabilities])

	#print classifications
	return classifications
