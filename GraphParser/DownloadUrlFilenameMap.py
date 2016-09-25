# DownloadUrlFilenameMap.py
import socket
import urllib
from DecoratorRetry import retry
from Defaults import DOWNLOAD_TIMEOUT
from Functions import segmentIDtoListID

# fail > @retry(Exception, tries=2, delay=1, backoff=0)
# ok > @retry(Exception, tries=4, delay=3, backoff=2)

@retry(Exception, tries=4, delay=3, backoff=2)
def urlretrieve_with_retry(url, filename):
    return urllib.urlretrieve(url, filename)

def DownloadUrlFilenameMap(FilenameMap, Segments):
    '''
    Download multiple files according to the FilenameMap.
    List of tripples in [ (<url>, <filename>, <edge id>), ... ]

    Marks entires in Segments with flags about the images.
    Returns list of failed downloads
    '''

    # timeout in seconds
    socket.setdefaulttimeout(DOWNLOAD_TIMEOUT)
    FailedSegmentImageDownloads = []

    for fileTuple in FilenameMap:
        url = fileTuple[0]
        filename = fileTuple[1]
        segment_id = fileTuple[2]
        segment_list_id = segmentIDtoListID(segment_id)

        print filename

        Segments[segment_list_id].HasLoadedImage = [True]
        
        try:
            urlretrieve_with_retry(url, filename)
        except:
            Segments[segment_list_id].HasLoadedImage = [False]
            FailedSegmentImageDownloads.append(segment_id)
            print "Failed to finally save the file."
            
    
    return [FailedSegmentImageDownloads]


# Exception example:
'''
images/078.jpg
Exception:  [Errno socket error] [Errno 11001] getaddrinfo failed
Exception:  [Errno socket error] timed out
'''
