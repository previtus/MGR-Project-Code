def StatisticsSegments(Segments):
    '''
    Provide statistics for loaded dataset
    :param Segments: input list of Segments
    '''
    # variables we are looking at:
    num_of_segments = len(Segments)
    num_of_potential_images = 0

    num_not_found_images = 0
    num_attractivity_not_known = 0  # score == -1
    num_valid = 0 # aka has images AND has scores

    num_attractivity_known = 0
    num_found_images = 0

    for Segment in Segments:
        for i_th_image in range(0,Segment.number_of_images):
            # Count for each image
            if Segment.hasUnknownScore():
                num_attractivity_not_known += 1
            else:
                num_attractivity_known += 1

            if not Segment.hasLoadedImageI(i_th_image):
                num_not_found_images += 1
            else:
                num_found_images += 1

            if (not Segment.hasUnknownScore()) and (Segment.hasLoadedImageI(i_th_image)):
                num_valid += 1

            num_of_potential_images += 1


    print "Segments Statistics:"
    print "From ", num_of_segments, " loaded Segments (with", num_of_potential_images, "potential images), only ", num_found_images, " have images (", num_not_found_images,"don't) and only ", num_attractivity_known, " have score (",num_attractivity_not_known,"don't)."
    print "The data set which we can use for training (aka has images AND has scores) is ", num_valid

'''
# Examples of usage
from DataOperations import *
Segments = LoadDataFile('../'+DATASTRUCTUREFILE)
StatisticsSegments(Segments)

UsableTrainSubset = SubsetSegments(Segments, has_image=True, has_score=True)
StatisticsSegments(UsableTrainSubset)
'''
