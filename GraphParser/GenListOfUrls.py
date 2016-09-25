# GenListOfUrls.py
from GraphEdgeSegment import *
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
        filename = "".join(["images/", format(segment.SegmentId, NUMBER_OF_ZEROS_PADDING), ".jpg"])

        if verbose: print url, '\n', filename, '\n'
        #print filename
        
        FilenameMap.append((url,filename,segment.SegmentId))

    return FilenameMap
