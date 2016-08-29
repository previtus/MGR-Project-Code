import urllib

def DownloadUrlFilenameMap(FilenameMap):
    '''
    Download multiple files according to the FilenameMap.
    List of tuples in [ (<url>, <filename>), ... ]
    '''

    for fileTuple in FilenameMap:
        url = fileTuple[0]
        filename = fileTuple[1]

        print filename

        # TODO: something more reliable than urlretrieve - with error handling, reconnections after some time etc.
        urllib.urlretrieve(url, filename)
    
    return []


