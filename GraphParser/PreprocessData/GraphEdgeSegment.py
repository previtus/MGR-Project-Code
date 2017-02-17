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

    def __init__(self, FromId, ToId, Nodes, SegmentId):
        '''
        Old initiation - we don't really need FromId or ToId to be saved...
        '''
        self.FromId = FromId
        self.ToId = ToId
        self.SegmentId = SegmentId

        self.Score = 0

        # Array of boolean flags if the images have been downloaded (1 or more)
        self.HasLoadedImage = [False]
        # Error code encountered while downloading
        self.ErrorMessage = ERROR_MESSAGE_NO_ERROR  # = -1

        # Latitude,Latitude projected,Longitude,Longitude projected,Elevation
        # self.Start = map(float, Nodes[FromId])
        # self.End = map(float, Nodes[ToId])
        self.Start = (float(Nodes[FromId][0]), float(Nodes[FromId][2]))
        self.End = (float(Nodes[ToId][0]), float(Nodes[ToId][2]))

        self.ProjectedStart = (float(Nodes[FromId][1]), float(Nodes[FromId][3]))
        self.ProjectedEnd = (float(Nodes[ToId][1]), float(Nodes[ToId][3]))

        self.ElevationStart = float(Nodes[FromId][4])
        self.ElevationEnd = float(Nodes[ToId][4])

        GraphEdgeSegment.tmp += 1

    def __init__(self, Start, End, Score, SegmentId):
        '''
        New initiation - from new dataset, where we might not even know node ids (we don't need them)
        '''
        self.FromId = -100
        self.ToId = -100
        self.SegmentId = SegmentId

        self.Score = Score

        # Array of boolean flags if the images have been downloaded (1 or more)
        self.HasLoadedImage = [False]
        # Error code encountered while downloading
        self.ErrorMessage = ERROR_MESSAGE_NO_ERROR  # = -1

        self.Start = Start
        self.End = End

        GraphEdgeSegment.tmp += 1

    def displaySegment(self):
        #print "SegmentId: ", self.SegmentId, "From: ", self.FromId,  ", To: ", self.ToId, ", Images: ", self.HasLoadedImage
        print "SegmentId: ", self.SegmentId, ", Images: ", self.HasLoadedImage, ", Score: ", self.getScore()
        print "Start: ", self.Start
        print "End: ", self.End

    def displaySegmentShort(self):
        #print "SegmentId: ", self.SegmentId, "From: ", self.FromId,  ", To: ", self.ToId, ", Images: ", self.HasLoadedImage
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

    def hasUnknownScore(self):
        return (self.getScore() == -1)

    def isValidSegment(self):
        return (self.hasLoadedImage()) and (not self.hasUnknownScore())