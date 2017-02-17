def StatisticsSegments(Segments):
    '''
    Provide statistics for loaded dataset
    :param Segments: input list of Segments
    '''
    # variables we are looking at:
    num = len(Segments)
    num_not_found_images = 0
    num_attractivity_not_known = 0  # score == -1
    num_valid = 0 # aka has images AND has scores

    for Segment in Segments:
        if Segment.hasUnknownScore():
            num_attractivity_not_known += 1
        if not Segment.hasLoadedImage():
            num_not_found_images += 1
        if (not Segment.hasUnknownScore()) and (Segment.hasLoadedImage()):
            num_valid += 1

    num_attractivity_known = num - num_attractivity_not_known  # score <> -1
    num_found_images = num - num_not_found_images

    print "Segments Statistics:"
    print "From ", num, " loaded Segments, only ", num_found_images, "(", num_not_found_images,"don't) have images and only ", num_attractivity_known, " have score (",num_attractivity_not_known,"don't)."
    print "The data set which we can use for training (aka has images AND has scores) is ", num_valid

def SubsetSegments(Segments, has_image=True, has_score=True):
    '''
    Function to filter amongst downloaded Segments. We can specify which kinds of Segments we want.
    Parameters can either require for example images present has_image=True, or on the contrary only those without
    images has_image=False, or ignore the fact has_image=None

    has_image=True - include only those with images
    has_image=False - include only those WITHOUT images
    has_image=None - include those with or without images (aka ignore the parameter)

    Example:
        UsableTrainSubset = SubsetSegments(Segments, has_image=True, has_score=True)
        StatisticsSegments(UsableTrainSubset)
        # Will give us only Segments which have images and scores - those we can use as training set

    :param Segments: Initial set of all segments
    :param needs_image: Whether to filter out those which don't have images
    :param needs_score: Whether to filter out those which don't have score
    :return: Returns the subset
    '''

    Subset = []
    for Segment in Segments:
        # Either - has image when it needs it || or we don't care || or it doesn't have image when we don't want it to have image
        if (has_image and Segment.hasLoadedImage()) or (has_image == None) or (not has_image and not Segment.hasLoadedImage()):
            # Similarly with scores
            if (has_score and not Segment.hasUnknownScore()) or (has_score == None) or (not has_score and Segment.hasUnknownScore()):
                Subset.append(Segment)

    return Subset


'''
# Examples of usage
from DataOperations import *
Segments = LoadDataFile('../'+DATASTRUCTUREFILE)
StatisticsSegments(Segments)

UsableTrainSubset = SubsetSegments(Segments, has_image=True, has_score=True)
StatisticsSegments(UsableTrainSubset)
'''
