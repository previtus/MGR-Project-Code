# DataOperations.py
import pickle
from PreprocessData.GenListOfUrls import *
from PreprocessData.DownloadUrlFilenameMap import *


''' todo: return false/true and take into account fails  '''

def SaveDataFile(name, Segments):
    '''
    Save structure of Segments into file <name>
    '''
    with open(name, 'wb') as f:
        pickle.dump(Segments, f)
        print "Saved |", len(Segments), "| segments."

def LoadDataFile(name):
    '''
    Load Segments from the file <name>
    '''
    Segments = []
    with open(name) as f:
        Segments = pickle.load(f)

    print "Loaded |", len(Segments), "| segments."
    return Segments

def MarkSegmentsWithImagesOfMD5(Segments, MD5, MARKERR):
    counter = 0
    for segment in Segments:
        for i_th_image in range(0, segment.number_of_images):
            image_url = segment.getImageFilename(i_th_image)
            # load img
            img = 0

            # md5 img
            md5_img = md5(img)

            # compare and mark segment errorneous
            if md5_img == MD5:
                segment.ErrorMessages[i_th_image] = MARKERR
                counter += 1
    print "Marked with error", MARKERR, " - ", counter, "images."


def HasSomeErrorneousData(Segments, ERROR_TYPE):
    '''
    Check for errors. Example:
    if (HasSomeErrorneousData(Segments,E)):
        Segments = FixDataFile_FailedDownloads(_,E)
    '''
    for segment in Segments:
        for i_th_image in range(0, segment.number_of_images):
            if segment.ErrorMessages[i_th_image] == ERROR_TYPE:
                return True
    return False

# todo version with directly Segments:
# > FixDataFile_FailedDownloads(___, ERROR_TYPE):

def FixDataFile_FailedDownloads(name, ERROR_TYPE):
    '''
    Loads, fixes and saves the structure of Segments. Looks at those
    with particular error messages ERROR_TYPE and redownloads images.
    Returns fixed Segments while it also saves them.
    
    Error codes in Default.py:
        - ERROR_MESSAGE_NOT_FOUND = 404
        - ERROR_MESSAGE_FAILED_MANY_TIMES = 101

    Eample call:
        FixDataFile_FailedDownloads(DATASTRUCTUREFILE, ERROR_MESSAGE_FAILED_MANY_TIMES)
    '''
    # load
    Segments = LoadDataFile(name)
    # bakname = "".join([name, ".bak"])
    # SaveDataFile(bakname, Segments)

    '''print "BEFORE:"
    for segment in Segments:
        segment.displaySegment()'''

    # fix
    BrokenSegments = []
    for segment in Segments:
        broken = False
        #print segment.ErrorMessage
        for i_th_image in range(0, segment.number_of_images):
            if segment.ErrorMessages[i_th_image] == ERROR_TYPE:
                broken = True
                #print segment.SegmentId
        if broken:
            BrokenSegments.append(segment)

    # Redownload the whole segment in such case...
            
    #print "BrokenSegments: ", BrokenSegments
    print "Fixing |", len(BrokenSegments), "| Segments."
    FilenameMapOfBroken = GenListOfUrls(BrokenSegments)
    #print "FilenameMapOfBroken: ", FilenameMapOfBroken
    F = DownloadUrlFilenameMap(FilenameMapOfBroken, Segments)
    
    '''print "AFTER:"
    for segment in Segments:
        segment.displaySegment()'''

    
    # save
    SaveDataFile(name, Segments)

    return Segments

'''
try with this > import cPickle as pickle
In all these cases, pickle and cPickle can fail you horribly.

If you are looking to save an object (arbitrarily created), where you have attributes (either added in the object
definition, or afterward)... your best bet is to use dill, which can serialize almost anything in python.
 >> Try Dill ?? maybe

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

# sample usage
save_object(company1, 'company1.pkl')
'''