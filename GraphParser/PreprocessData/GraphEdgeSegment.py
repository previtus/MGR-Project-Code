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
        self.HasLoadedImage = [False]
        # Error code encountered while downloading
        self.ErrorMessages = [ERROR_MESSAGE_NO_ERROR]  # = -1

        self.Start = Start
        self.End = End

        GraphEdgeSegment.tmp += 1

    def ScoreAdjustment(self,val):
        # val goes <0,100> we want <0,1> (when using sigmoid)
        return (float(val)/100.0)

    def setScore(self, s):
        self.Score = self.ScoreAdjustment(s)

    def displaySegment(self):
        print "SegmentId: ", self.SegmentId, ", Images: ", self.HasLoadedImage, ", Score: ", self.getScore()
        print "Start: ", self.Start
        print "End: ", self.End

    def displaySegmentShort(self):
        print "SegmentId: ", self.SegmentId, ", Images: ", self.HasLoadedImage, ", Score: ", self.getScore()

    def getBearingString(self):
        return bearing_between_two_points(self.Start, self.End)

    def getGoogleViewUrl(self,resx,resy):
        'Google View url from the start of this segment'
        # http://maps.googleapis.com/maps/api/
        # streetview?size=600x400&location=<lat>,<long>&heading=<angle from north>&key=<api>
        lat = self.Start[0]
        lon = self.Start[1]
        bearing = round(self.getBearingString(), 2)
        url_start = "http://maps.googleapis.com/maps/api/streetview?size="
        api = getApi()

        full_url = [url_start, str(resx), "x", str(resy), "&location=", str(lat), ",", str(lon), "&heading=", str(bearing), "&key=", api]

        return "".join(full_url)

    def getImageFilename(self):
        'Unified filename generation'
        filename = "".join(["Data/images/", format(self.SegmentId, NUMBER_OF_ZEROS_PADDING), ".jpg"])
        return filename

    def getScore(self):
        return self.Score

    def hasLoadedImage(self):
        # while working with one image only, the validity flag is if we got it
        return self.HasLoadedImage[0]

    def hasLoadedImageI(self, i):
        # while working with one image only, the validity flag is if we got it
        return self.HasLoadedImage[i]

    def hasUnknownScore(self):
        return (self.getScore() == -1)

    def isValidSegment(self):
        return (self.hasLoadedImage()) and (not self.hasUnknownScore())