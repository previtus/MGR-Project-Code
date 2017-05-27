# DataOperations.py
import pickle
from PreprocessData.GenListOfUrls import *
from PreprocessData.DownloadUrlFilenameMap import *
from PreprocessData.SegmentObj import *

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


    try:
        with open(name,'rb') as f:
            Segments = pickle.load(f)
    except:
        print "Failed opening file at", name


    print "Loaded |", len(Segments), "| segments."
    return Segments

def MarkBadSegments(Segments, MD5_list, MARKERR):
    '''
    Used to manually mark bad segments after they are downloaded (using the rest of the set and not having to
    re-download it all).
    Ps: all of the known errors we mark directly while downloading in DownloadUrlFilenameMap

    Example call:
    # manual marking and saving
    #Segments = MarkSegmentsWithImagesOfMD5(Segments, QUOTA_EXCEEDED_CHECKSUM, ERROR_MESSAGE_QUOTA)
    #SaveDataFile(DATASTRUCTUREFILE, Segments)

    :param Segments: Input segments (remember to save them after! and possibly back them up before)
    :param MD5_list: we are looking for certain md5 of the image - for example "b2328ec7ff935944a85723daddf0e8b7" was quota
    :param MARKERR: we want to mark the *bad* segments - we will thus force all the photos related to one Segment to redownload
    :return: Edited Segments, remember to save them.
    '''
    counter = 0
    for segment in Segments:
        for i_th_image in range(0, segment.number_of_images):
            if segment.hasLoadedImageI(i_th_image):
                image_url = segment.getImageFilename(i_th_image)

                # md5 img
                md5_img = md5(image_url)
                # print md5_img
                if md5_img == -1:
                    segment.ErrorMessages[i_th_image] = MARKERR
                    counter += 1
                else:
                    for MD5 in MD5_list:
                        # compare and mark segment errorneous
                        if md5_img == MD5:
                            segment.ErrorMessages[i_th_image] = MARKERR
                            counter += 1
    print "Marked with error <", MARKERR, "> - ", counter, "images."
    return Segments

def HasSomeErrorneousData(Segments, ERROR_TYPE):
    '''
    Check for errors. Example:
    if (HasSomeErrorneousData(Segments,E)):
        Segments = FixDataFile_FailedDownloads(_,E)
    '''
    for segment in Segments:
        for i_th_image in range(0, len(segment.ErrorMessages)):
            #print segment.ErrorMessages[i_th_image]
            if segment.ErrorMessages[i_th_image] == ERROR_TYPE:
                return True
    return False

# todo version with directly Segments:
# > FixDataFile_FailedDownloads(___, ERROR_TYPE):

def FixDataFile_FailedDownloads(name, ERROR_TYPE, PIXELS_X, PIXELS_Y, PrependPath):
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
                segment.LocationsIndex = []
                #print segment.SegmentId
        if broken:
            BrokenSegments.append(segment)

    # Redownload the whole segment in such case...
            
    #print "BrokenSegments: ", BrokenSegments
    print "Fixing |", len(BrokenSegments), "| Segments."
    FilenameMapOfBroken = GenListOfUrls(BrokenSegments, PIXELS_X, PIXELS_Y, PrependPath)
    print "Equals to |", len(FilenameMapOfBroken), "| Images."

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

def save_segments_file_as_without_missing_files(in_segments_file, path_to_images, out_segments_file):
    # Special treatment of Segments file - mark all missing images as unusable
    # ... we don't want to redownload them, as these have been manually deleted as too >bonkers<. (understand: outliers)
    Segments = LoadDataFile(in_segments_file)

    print "Segments may have nonexistent files linked:"
    for Segment in Segments:
        for i_th_image in range(0,Segment.number_of_images):

            if Segment.hasLoadedImageI(i_th_image):
                # Additional filtering - if we cant find the image, don't include it
                # this is useful for manual deleting of images

                filename = path_to_images+Segment.getImageFilename(i_th_image)

                import os.path
                if not os.path.isfile(filename):
                    print filename
                    Segment.HasLoadedImages[i_th_image] = False

    print "Now shouldn't:"
    for Segment in Segments:
        for i_th_image in range(0,Segment.number_of_images):

            if Segment.hasLoadedImageI(i_th_image):
                # Additional filtering - if we cant find the image, don't include it
                # this is useful for manual deleting of images

                filename = path_to_images+Segment.getImageFilename(i_th_image)

                import os.path
                if not os.path.isfile(filename):
                    print filename
                    Segment.HasLoadedImages[i_th_image] = False

    SaveDataFile(out_segments_file, Segments)


def save_segments_file_marking_missing_files_as_errors(in_segments_file, path_to_images, out_segments_file):
    Segments = LoadDataFile(in_segments_file)

    print "Segments may have nonexistent files linked:"
    for Segment in Segments:
        for i_th_image in range(0,Segment.number_of_images):

            if Segment.hasLoadedImageI(i_th_image):
                # Additional filtering - if we cant find the image, don't include it
                # this is useful for manual deleting of images

                filename = path_to_images+Segment.getImageFilename(i_th_image)

                import os.path
                if not os.path.isfile(filename):
                    print filename
                    Segment.ErrorMessages[i_th_image] = ERROR_MESSAGE_QUOTA

    SaveDataFile(out_segments_file, Segments)

'''
in_segments_file = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_minlen30_640px/SegmentsData.dump'
path_to_images = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_minlen30_640px/'
out_segments_file = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_minlen30_640px/SegmentsData.dump'
save_segments_file_marking_missing_files_as_errors(in_segments_file, path_to_images, out_segments_file)
'''

'''
keep files:
SegmentsData_invalid.dump
SegmentsData_marked_R100_4Tables_invalid.dump
SegmentsData_marked_R100_invalid.dump
SegmentsData_marked_R200_4Tables_invalid.dump
SegmentsData_marked_R50_4Tables_invalid.dump
'''
