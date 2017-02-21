# GraphEdgeSegment.py
from Functions import *
import sys
sys.path.append('..')
from Defaults import *

class GraphEdgeSegment:
    '''
    Common base class for segment
    Variables: FromId, ToId, SegmentId
    Functions: getBearingString(), getGoogleViewUrl()
    '''
    tmp = 0

    def __init__(self, Start, End, Score, SegmentId):
        '''
        Initialize Segment with the data from an edge.
        :param Start: start coordinates
        :param End: end coordinates
        :param Score: score, which is then transformed
        :param SegmentId: segment unique id
        '''
        self.SegmentId = SegmentId

        self.setScore(Score)

        # Array of boolean flags if the images have been downloaded (1 or more)
        self.HasLoadedImages = []
        # Error code encountered while downloading
        self.ErrorMessages = []  # = -1

        self.number_of_images = 0

        self.Start = Start
        self.End = End

        GraphEdgeSegment.tmp += 1

    def ScoreAdjustment(self,val):
        # val goes <0,100> we want <0,1> (when using sigmoid)
        return (float(val)/100.0)

    def setScore(self, s):
        self.Score = self.ScoreAdjustment(s)

    def displaySegment(self):
        print "SegmentId: ", self.SegmentId, ", Images: ", self.HasLoadedImages, ", Score: ", self.getScore()
        print "Start: ", self.Start
        print "End: ", self.End

    def displaySegmentShort(self):
        print "SegmentId: ", self.SegmentId, ", Images: ", self.HasLoadedImages, ", Score: ", self.getScore()

    def getBearingString(self, Location, Direction):
        return bearing_between_two_points(Location, Direction)

    def resetImageMemory(self, number_of_images):
        self.number_of_images = number_of_images
        for i in range(0,number_of_images):
            self.HasLoadedImages.append(False)
            self.ErrorMessages.append(ERROR_MESSAGE_NO_ERROR)

    def getGoogleViewUrls(self,resx,resy):
        '''
        Generate urls for the Segment. Here we also reset the
        :param resx: Resolution of images, X
        :param resy: Resolution of images, Y
        :return: returns list of urls and filenames to download
        '''

        urls = []
        filenames = []

        # Looking from START to END
        urls.append( self.getGoogleViewUrl(self.Start, self.End, PIXELS_X,PIXELS_Y) )
        filenames.append( self.getImageFilename(len(filenames)) )

        # Looking from END to START
        urls.append( self.getGoogleViewUrl(self.End, self.Start, PIXELS_X,PIXELS_Y) )
        filenames.append( self.getImageFilename(len(filenames)) )

        # And more to come <3

        number_of_images = len(urls)
        self.resetImageMemory(number_of_images)

        return [urls, filenames]

    def getGoogleViewUrl(self, Location, Direction, resx, resy):
        'Google View url from the start of this segment'
        # http://maps.googleapis.com/maps/api/
        # streetview?size=600x400&location=<lat>,<long>&heading=<angle from north>&key=<api>
        lat = Location[0]
        lon = Location[1]
        bearing = round(self.getBearingString(Location, Direction), 2)
        url_start = "http://maps.googleapis.com/maps/api/streetview?size="
        api = getApi()

        full_url = [url_start, str(resx), "x", str(resy), "&location=", str(lat), ",", str(lon), "&heading=", str(bearing), "&key=", api]

        return "".join(full_url)

    def getImageFilename(self, i_th_image):
        'Unified filename generation'
        filename = "".join(["Data/images/", format(self.SegmentId, NUMBER_OF_ZEROS_PADDING), "_", str(i_th_image), ".jpg"])
        return filename

    def getScore(self):
        return self.Score

    def hasLoadedImageI(self, i):
        # while working with one image only, the validity flag is if we got it
        return self.HasLoadedImages[i]

    def hasUnknownScore(self):
        return (self.getScore() == -1)
