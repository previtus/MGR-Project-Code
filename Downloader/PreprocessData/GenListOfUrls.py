# GenListOfUrls.py
import sys
sys.path.append('..')

def GenListOfUrls(Segments, PIXELS_X, PIXELS_Y, PrependPath='', minimal_length=20, custom=False):
    '''
    Iterates over the segment list and returns a list of urls needed for download
    Outputs list of tripples in [ (<url>, <filename>, <edge id>), ... ]
    '''
    
    FilenameMap = []
    verbose = False

    num_of_segments_with_score = 0
    num_of_image_urls_to_attempt_to_down = 0
    for segment in Segments:
        
        if verbose: segment.displaySegment()

        if custom or not segment.hasUnknownScore():
            # We only care about scored segments now...
            num_of_segments_with_score += 1

            if custom:
                [urls, filenames] = segment.getGoogleViewUrls(PIXELS_X,PIXELS_Y)
            else:
                [urls, filenames] = segment.getGoogleViewUrls_whileUsingFractionsOfMinEdgeLen(PIXELS_X, PIXELS_Y, minimal_length)

            #print len(urls), urls
            num_of_image_urls_to_attempt_to_down += len(urls)

            for i_nth_image in range(0, len(urls)):
                if verbose: print urls, '\n', filenames, '\n'
                #print filenames[i_nth_image]

                FilenameMap.append((urls[i_nth_image], PrependPath+filenames[i_nth_image], segment.SegmentId, i_nth_image))

    print "num_of_segments_with_score", num_of_segments_with_score
    print "num_of_image_urls_to_attempt_to_down", num_of_image_urls_to_attempt_to_down
    return FilenameMap
