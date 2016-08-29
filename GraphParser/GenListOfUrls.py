from GraphEdgeSegment import *
from Defaults import *

def GenListOfUrls(Segments):
    
    FilenameMap = []
    verbose = False

    for segment in Segments:
        
        if verbose: segment.displaySegment()
        url = segment.getGoogleViewUrl(600,400)
        filename = "".join(["images/", format(segment.SegmentId, NUMBER_OF_ZEROS_PADDING), ".jpg"])

        if verbose: print url, '\n', filename, '\n'
        #print filename
        
        FilenameMap.append((url,filename))

    return FilenameMap
