# GenListOfUrls.py
from GraphEdgeSegment import *
import sys
sys.path.append('..')
from Downloader.Defaults import *

def GenListOfUrls(Segments):
    '''
    Iterates over the segment list and returns a list of urls needed for download
    Outputs list of tripples in [ (<url>, <filename>, <edge id>), ... ]
    '''
    
    FilenameMap = []
    verbose = False

    for segment in Segments:
        
        if verbose: segment.displaySegment()

        [urls, filenames] = segment.getGoogleViewUrls(PIXELS_X,PIXELS_Y)

        for i_nth_image in range(0, len(urls)):
            if verbose: print urls, '\n', filenames, '\n'
            # print filename

            FilenameMap.append((urls[i_nth_image], filenames[i_nth_image], segment.SegmentId, i_nth_image))

    return FilenameMap
