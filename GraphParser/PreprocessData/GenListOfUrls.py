# GenListOfUrls.py
from GraphEdgeSegment import *
import sys
sys.path.append('..')
from Defaults import *

def GenListOfUrls(Segments):
    '''
    Iterates over the segment list and returns a list of urls needed for download
    Outputs list of tripples in [ (<url>, <filename>, <edge id>), ... ]
    '''
    
    FilenameMap = []
    verbose = False

    for segment in Segments:
        
        if verbose: segment.displaySegment()
        url = segment.getGoogleViewUrl(PIXELS_X,PIXELS_Y)
        filename = segment.getImageFilename()

        if verbose: print url, '\n', filename, '\n'
        #print filename
        
        FilenameMap.append((url,filename,segment.SegmentId))

    return FilenameMap
