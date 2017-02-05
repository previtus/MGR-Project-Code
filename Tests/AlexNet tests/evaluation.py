PATH_TO_CONVNETS_KERAS = '/home/ekmek/TEMP_SPACE/convnets-keras/' #not pretty
import sys
sys.path.insert(0, PATH_TO_CONVNETS_KERAS)
from convnetskeras.imagenet_tool import id_to_synset

def evaluation( groundtruth_file, classification_list, topNerror ):
	"""
	Gets Top-N error from the classifications in <classification_list> and ground truth.
	      
	(( classification_list / classification_file which would load into the list ))

	format:
	classification_list:
		[[image number, [N labels], [N probabilities]], ...etc.]
		(ps: probabilities are skipped now, we don't use them)

	groundtruth_file:
		line number => the ground truth for image with number of the line
		(so line number 1 refers to ILSVRC2010_val_00000001.JPEG
	"""

	# DEBUG!
	d = {}
	with open("/home/ekmek/TEMP_SPACE/convnets-keras/words.txt") as f:
		for line in f:
			arr = line.split()
			key = arr[0]
			val = " ".join(arr[1:])
			#print key, val
			d[key] = val
	

	# load groundtruth_list
	with open(groundtruth_file) as f:
	    groundtruth_list = f.readlines()
	groundtruth_list = [-1] + [int(x.strip()) for x in groundtruth_list] 
	#print groundtruth_list[0:10]
	
	# for image_number true label look at => groundtruth_list[image_number]
	for item in classification_list:
		# print item
		image_number = item[0]
		labels = item[1]
		#probabilites = item[2]
		ground_truth = groundtruth_list[image_number]

		# DEBUG!
		print "img", image_number, item[3], "is", ground_truth, d[id_to_synset(ground_truth)], "in", labels, ground_truth in labels
		

	return []