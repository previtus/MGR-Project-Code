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

def LoadDataFile(name, only_valid=False):
    '''
    Load Segments from the file <name>
    '''
    Segments = []
    with open(name) as f:
        Segments = pickle.load(f)

    if (only_valid):
        # Delete not valid Segments
        ValidSegments = []
        for Segment in Segments:
            if not Segment.isValidSegment():
                Segments.remove(Segment)

            #if Segment.isValidSegment():
                #ValidSegments.append(Segment)
        #Segments = ValidSegments

    print "Loaded |", len(Segments), "| segments."
    return Segments

def HasSomeErrorneousData(Segments, ERROR_TYPE):
    '''
    Check for errors. Example:
    if (HasSomeErrorneousData(Segments,E)):
        Segments = FixDataFile_FailedDownloads(_,E)
    '''
    for segment in Segments:
        if segment.ErrorMessage == ERROR_TYPE:
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
        #print segment.ErrorMessage
        if segment.ErrorMessage == ERROR_TYPE:
            #print segment.SegmentId
            BrokenSegments.append(segment)
            
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
