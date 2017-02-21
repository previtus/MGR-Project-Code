# DownloadUrlFilenameMap.py
import sys
sys.path.append('..')
from Defaults import *

import socket
import urllib
import hashlib
import os
from DecoratorRetry import retry
from Functions import segmentIDtoListID

# fail > @retry(Exception, tries=2, delay=1, backoff=0)
# ok > @retry(Exception, tries=4, delay=3, backoff=2)

@retry(Exception, tries=5, delay=0.3, backoff=1)
def urlretrieve_with_retry(url, filename):
    ''' Saves (image) file and returns (<filename_string>, <object of httplib.HTTPMessage>) '''
    return urllib.urlretrieve(url, filename)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def DownloadUrlFilenameMap(FilenameMap, Segments):
    '''
    Download multiple files according to the FilenameMap.
    List of tripples in [ (<url>, <filename>, <edge id>), ... ]

    Marks entires in Segments with flags about the images.
    Returns list of failed downloads
    '''

    # Check for the target directory
    filename = FilenameMap[0][1]
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # timeout in seconds
    socket.setdefaulttimeout(DOWNLOAD_TIMEOUT)
    FailedSegmentImageDownloads = []

    for fileTuple in FilenameMap:
        url = fileTuple[0]
        filename = fileTuple[1]
        segment_id = fileTuple[2]
        i_nth_image = fileTuple[3]
        segment_list_id = segmentIDtoListID(segment_id)

        Segments[segment_list_id].ErrorMessages[i_nth_image] = ERROR_MESSAGE_NO_ERROR
        isLoaded = True
        md5_code = ""
        
        try:
            image_header = urlretrieve_with_retry(url, filename)
            md5_code = md5(image_header[0])
            
            if (md5_code == FILE_NOT_FOUND_CHECKSUM):
                # HANDLE PHOTO NOT FOUND / INVALID SEGMENT
                isLoaded = False
                print "No photographic information on the spot."
                os.remove(image_header[0])
                FailedSegmentImageDownloads.append([segment_id, i_nth_image])
                # remove invalid segments?
                # better have dictionary dict[ID] => obj
                ## not del Segments[segment_id]
                Segments[segment_list_id].ErrorMessages[i_nth_image] = ERROR_MESSAGE_NOT_FOUND #404
            
        except Exception, e:
            # HANDLE FAIL OF DOWNLOADING PHOTO / INVALID SEGMENT
            print "exception: ", str(e)
            isLoaded = False
            FailedSegmentImageDownloads.append([segment_id, i_nth_image])
            # remove invalid segments?
            Segments[segment_list_id].ErrorMessages[i_nth_image] = ERROR_MESSAGE_FAILED_MANY_TIMES #101


            print "Failed to finally save the file."

        Segments[segment_list_id].HasLoadedImages[i_nth_image] = isLoaded
        print filename, md5_code, isLoaded
    
    return [FailedSegmentImageDownloads]


# Exception example:
'''
images/078.jpg
Exception:  [Errno socket error] [Errno 11001] getaddrinfo failed
Exception:  [Errno socket error] timed out
'''
