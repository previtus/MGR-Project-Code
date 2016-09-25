# DownloadUrlFilenameMap.py
import socket
import urllib
from DecoratorRetry import retry
from Defaults import *

@retry(Exception, tries=8, delay=3, backoff=2)
def urlretrieve_with_retry(url, filename):
    return urllib.urlretrieve(url, filename)

def DownloadUrlFilenameMap(FilenameMap):
    '''
    Download multiple files according to the FilenameMap.
    List of tripples in [ (<url>, <filename>, <edge id>), ... ]
    '''

    # timeout in seconds
    socket.setdefaulttimeout(DOWNLOAD_TIMEOUT)


    for fileTuple in FilenameMap:
        url = fileTuple[0]
        filename = fileTuple[1]
        segment_id = fileTuple[2]

        print filename

        urlretrieve_with_retry(url, filename)
    
    return []


# Exception example:
'''
images/078.jpg
Exception:  [Errno socket error] [Errno 11001] getaddrinfo failed
Exception:  [Errno socket error] timed out
'''
