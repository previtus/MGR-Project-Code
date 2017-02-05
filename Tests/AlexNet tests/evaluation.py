def evaluation( groundtruth_file, classification_file, topNerror ):
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

	# load classification_list
	with open(classification_file) as f:
                classification_list = f.readlines()
        classification_list = [map(int,x.strip().split()) for x in classification_list] 
        #print classification_list[0:10]

	# load groundtruth_list
	with open(groundtruth_file) as f:
	    groundtruth_list = f.readlines()
	groundtruth_list = [-1] + [int(x.strip()) for x in groundtruth_list] 
	#print groundtruth_list[0:10]

        summ = 0
        div = 0
	# for image_number true label look at => groundtruth_list[image_number]
	for item in classification_list:
		# print item
		image_number = item[0]
		labels = item[1:]
		ground_truth = groundtruth_list[image_number]

                if not(ground_truth in labels):
                        summ += 1
                div += 1
                
		# DEBUG!
		#print image_number, labels

        error_rate = 100.0*(float(summ) / float(div))
        print "".join(["Top-",str(topNerror),"-error :"]), error_rate, "%"
	
	return []
