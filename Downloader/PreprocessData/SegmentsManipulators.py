def StatisticsSegments(Segments, additionalStatistics=False):
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

    if additionalStatistics:
        AdditionalStatistics(Segments)


'''
# Examples of usage
from DataOperations import *
Segments = LoadDataFile('../'+DATASTRUCTUREFILE)
StatisticsSegments(Segments)

UsableTrainSubset = SubsetSegments(Segments, has_image=True, has_score=True)
StatisticsSegments(UsableTrainSubset)
'''

def AdditionalStatistics(Segments):
    stats_over_d = []

    for Segment in Segments:
        d = 1000*distance_between_two_points(Segment.Start, Segment.End)
        #print d, Segment.Start, Segment.End
        stats_over_d.append(d)

        '''
        m = midpoint(Segment.Start, Segment.End)
        d1 = 1000 * distance_between_two_points(Segment.Start, m)
        d2 = 1000 * distance_between_two_points(m, Segment.End)
        print abs(d - (d1+d2)), d1, d2
        '''


    from DatasetHandler.DatasetVizualizators import *
    import numpy as np

    data = np.array(stats_over_d)
    min = np.amin(data)
    max = np.amax(data)
    mean = np.mean(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    print min, "|---[", q1, "{", mean, "}", q3, "]---|", max

    save_to_pdf = True
    plotWhisker(data, 'Lengths of edges (in meters)', y_min=min, y_max=max)
    plotHistogram(data, 'Length distribution histogram (in meters)', x_min=min, x_max=max, num_bins=30,
                custom_x_label='Distance in meters', custom_y_label='Count of occurances')
    plotX_sortValues(data, 'Lengths of edges (sorted, in meters)', x_min=min, x_max=max, notReverse=True,
                custom_x_label = '# of edge', custom_y_label = 'edge length in meters')
    if save_to_pdf:
        saveAllPlotsToPDF()
    show()

'''
file = '/home/ekmek/Desktop/MGR-Project-Code/Data/StreetViewData/1200x_markable_299x299/SegmentsData.dump'
from Downloader.DataOperations import *
Segments = LoadDataFile(file)
StatisticsSegments(Segments, True)
'''