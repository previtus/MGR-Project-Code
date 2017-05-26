# GraphEdgeSegment.py
from Functions import *
import sys
sys.path.append('..')
from Downloader.Defaults import *

class SegmentObj:
    '''
    Common base class for segment
    Variables: FromId, ToId, SegmentId
    Functions: getBearingString(), getGoogleViewUrl()
    '''

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

        # each of the i images has it's own location
        self.LocationsIndex = []
        self.DistinctLocations = []
        # ... and after as well its own Nearby vector
        self.DistinctNearbyVector = []
        # One segment can generate multiple images, where we "stand" and "look" at different positions, each of these
        # will have different central location associated.

        # PS: when we have 3 images based in Start and 3 based in End, we can reuse the values of neighborhood
        # (as long as we use cirle around the point as neighborhood)

        self.Segment_OSM_MARKING_VERSION = '-1'

    def ScoreAdjustment(self,val):
        # val goes <0,100> we want <0,1> (when using sigmoid)
        return (float(val)/100.0)

    def setScore(self, s):
        if s <> -1:
            self.Score = self.ScoreAdjustment(s)
        else:
            self.Score = s

    def displaySegment(self):
        print "SegmentId: ", self.SegmentId, ", Images: ", self.HasLoadedImages, ", Errors: ", self.ErrorMessages, ", Score: ", self.getScore()
        print "Start: ", self.Start
        print "End: ", self.End

    def displaySegmentShort(self):
        print "SegmentId: ", self.SegmentId, ", Images: ", self.HasLoadedImages, ", Score: ", self.getScore()

    def getBearingString(self, Location, Direction, degrees_offset=0.0):
        return bearing_between_two_points(Location, Direction, degrees_offset)

    def resetImageMemory(self, number_of_images):
        self.HasLoadedImages = []
        self.ErrorMessages = []
        self.number_of_images = number_of_images
        for i in range(0,number_of_images):
            self.HasLoadedImages.append(False)
            self.ErrorMessages.append(ERROR_MESSAGE_NO_ERROR)

    def getGoogleViewUrls(self, PIXELS_X, PIXELS_Y):
        '''
        Generate urls for the Segment. Here we also reset the
        :param resx: Resolution of images, X
        :param resy: Resolution of images, Y
        :return: returns list of urls and filenames to download
        '''

        urls = []
        filenames = []

        # Looking from START to END
        self.DistinctLocations.append(self.Start) # we are standing in Start

        # 1 IMG
        urls.append(self.getGoogleViewUrl(self.Start, self.End, PIXELS_X, PIXELS_Y))
        filenames.append(self.getImageFilename(len(filenames)))
        self.LocationsIndex.append(0)

        '''
        # Turning around the spot on for the two end points:
        # Smart turns: START->END turn till 180 'right'
        split_into = 5.0 # will create (split_into-1) images
        degrees_turn = 180.0/split_into
        summ = degrees_turn
        while (summ < 180.0):
            urls.append(self.getGoogleViewUrl(self.Start, self.End, PIXELS_X, PIXELS_Y, degrees_offset=summ))
            filenames.append(self.getImageFilename(len(filenames)))
            summ += degrees_turn
        '''

        urls.append(self.getGoogleViewUrl(self.Start, self.End, PIXELS_X, PIXELS_Y, degrees_offset=120.0))
        filenames.append(self.getImageFilename(len(filenames)))
        self.LocationsIndex.append(0)
        urls.append(self.getGoogleViewUrl(self.Start, self.End, PIXELS_X, PIXELS_Y, degrees_offset=240.0))
        filenames.append(self.getImageFilename(len(filenames)))
        self.LocationsIndex.append(0)

        # Looking from END to START
        self.DistinctLocations.append(self.End) # we are standing in Start

        # 1 IMG
        urls.append( self.getGoogleViewUrl(self.End, self.Start, PIXELS_X,PIXELS_Y) )
        filenames.append( self.getImageFilename(len(filenames)) )
        self.LocationsIndex.append(1)

        '''
        # Smart turns: END->START turn till 180 'right'
        summ = degrees_turn
        while (summ < 180.0):
            urls.append(self.getGoogleViewUrl(self.End, self.Start, PIXELS_X, PIXELS_Y, degrees_offset=summ))
            filenames.append(self.getImageFilename(len(filenames)))
            summ += degrees_turn

        # COUNT = 2 + 2*(split_into-1) = 2 + 2*4 = 10 per one segment
        # 10 times the data? sounds pretty good
        '''

        urls.append( self.getGoogleViewUrl(self.End, self.Start, PIXELS_X,PIXELS_Y, degrees_offset=120.0))
        filenames.append(self.getImageFilename(len(filenames)))
        self.LocationsIndex.append(1)
        urls.append( self.getGoogleViewUrl(self.End, self.Start, PIXELS_X,PIXELS_Y, degrees_offset=240.0))
        filenames.append(self.getImageFilename(len(filenames)))
        self.LocationsIndex.append(1)

        # And more to come <3

        number_of_images = len(urls)
        self.resetImageMemory(number_of_images)

        for distLoc in self.DistinctLocations:
            self.DistinctNearbyVector.append(None)

        return [urls, filenames]

    def getGoogleViewUrl(self, Location, Direction, resx, resy, degrees_offset=0.0):
        'Google View url from the start of this segment'
        # http://maps.googleapis.com/maps/api/
        # streetview?size=600x400&location=<lat>,<long>&heading=<angle from north>&key=<api>
        lat = Location[0]
        lon = Location[1]
        bearing = round(self.getBearingString(Location, Direction, degrees_offset), 2)
        url_start = "http://maps.googleapis.com/maps/api/streetview?size="
        api = getApi()

        full_url = [url_start, str(resx), "x", str(resy), "&location=", str(lat), ",", str(lon), "&heading=", str(bearing), "&key=", api]

        return "".join(full_url)

    def getImageFilename(self, i_th_image):
        'Unified filename generation'
        filename = "".join(["images/", format(self.SegmentId, NUMBER_OF_ZEROS_PADDING), "_", str(i_th_image), ".jpg"])
        return filename

    def getScore(self):
        return self.Score

    def hasLoadedImageI(self, i):
        # while working with one image only, the validity flag is if we got it
        return self.HasLoadedImages[i]

    def hasUnknownScore(self):
        return (self.getScore() < 0) # negative score means unknown (-1 in source was /100)

    def getLocation(self, i_th_image):
        index = self.LocationsIndex(i_th_image)
        return self.DistinctLocations[index]

    def checkOSMVersion(self):
        print "Current project-wide OSM Marking version is: " + OSM_MARKING_VERSION + " | These Segments are on: " + self.Segment_OSM_MARKING_VERSION
        return (self.Segment_OSM_MARKING_VERSION == OSM_MARKING_VERSION)

    def getNearbyVector(self, i_th_image):
        if not self.checkOSMVersion():
            print "Warning, the Segment's OSM_MARKING_VERSION is not up to date, the NearbyVector structure might have changed!"
        index = self.LocationsIndex(i_th_image)
        return self.DistinctNearbyVector[index]

    def markWithVector(self, nearby_vector, index, MARKING_VERSION):
        self.DistinctNearbyVector[index] = nearby_vector
        self.Segment_OSM_MARKING_VERSION = MARKING_VERSION

    # ---------------------------------------------------------------------------------------------------------------------
    def betweenPoints(self, pointStart, pointEnd):
        urls = []
        filenames = []

        # Looking from START to END
        self.DistinctLocations.append(pointStart) # we are standing in Start
        k = len(self.DistinctLocations) - 1
        loaded_before = len(self.LocationsIndex)

        # 1 IMG
        urls.append(self.getGoogleViewUrl(pointStart, pointEnd, PIXELS_X, PIXELS_Y))
        filenames.append(self.getImageFilename(loaded_before+len(filenames)))
        self.LocationsIndex.append(k)

        '''
        # Turning around the spot on for the two end points:
        # Smart turns: START->END turn till 180 'right'
        split_into = 5.0 # will create (split_into-1) images
        degrees_turn = 180.0/split_into
        summ = degrees_turn
        while (summ < 180.0):
            urls.append(self.getGoogleViewUrl(pointStart, pointEnd, PIXELS_X, PIXELS_Y, degrees_offset=summ))
            filenames.append(self.getImageFilename(loaded_before+len(filenames)))
            summ += degrees_turn
        '''

        urls.append(self.getGoogleViewUrl(pointStart, pointEnd, PIXELS_X, PIXELS_Y, degrees_offset=120.0))
        filenames.append(self.getImageFilename(loaded_before+len(filenames)))
        self.LocationsIndex.append(k)
        urls.append(self.getGoogleViewUrl(pointStart, pointEnd, PIXELS_X, PIXELS_Y, degrees_offset=240.0))
        filenames.append(self.getImageFilename(loaded_before+len(filenames)))
        self.LocationsIndex.append(k)

        # Looking from END to START
        self.DistinctLocations.append(pointEnd) # we are standing in Start
        k = len(self.DistinctLocations) - 1

        # 1 IMG
        urls.append( self.getGoogleViewUrl(pointEnd, pointStart, PIXELS_X,PIXELS_Y) )
        filenames.append( self.getImageFilename(loaded_before+len(filenames)) )
        self.LocationsIndex.append(k)

        '''
        # Smart turns: END->START turn till 180 'right'
        summ = degrees_turn
        while (summ < 180.0):
            urls.append(self.getGoogleViewUrl(pointEnd, pointStart, PIXELS_X, PIXELS_Y, degrees_offset=summ))
            filenames.append(self.getImageFilename(loaded_before+len(filenames)))
            summ += degrees_turn

        # COUNT = 2 + 2*(split_into-1) = 2 + 2*4 = 10 per one segment
        # 10 times the data? sounds pretty good
        '''

        urls.append( self.getGoogleViewUrl(pointEnd, pointStart, PIXELS_X,PIXELS_Y, degrees_offset=120.0))
        filenames.append(self.getImageFilename(loaded_before+len(filenames)))
        self.LocationsIndex.append(k)
        urls.append( self.getGoogleViewUrl(pointEnd, pointStart, PIXELS_X,PIXELS_Y, degrees_offset=240.0))
        filenames.append(self.getImageFilename(loaded_before+len(filenames)))
        self.LocationsIndex.append(k)

        return urls, filenames

    def getGoogleViewUrls_novel_brainscratching_aproach_weee_ohyeah(self, PIXELS_X, PIXELS_Y, minimal_length):
        urls = []
        filenames = []

        min_allowed_distance = minimal_length

        d = 1000*distance_between_two_points(self.Start, self.End)
        number_of_splits = int(max((floor(d / min_allowed_distance)),1.0))

        #print "---", d, min_allowed_distance, number_of_splits

        before_frac = 0.0
        loc = 0

        for frac in range(0,number_of_splits):
            current_frac = (frac+1) * (1.0 / number_of_splits)

            # before_frac, current_frac will be 0.0-0.2, 0.2-0.4, etc all the way till 0.8-1.0
            PointA = interpolation(self.Start, self.End, fraction=before_frac)
            PointB = interpolation(self.Start, self.End, fraction=current_frac)
            #d = 1000*distance_between_two_points(PointA, PointB)
            #print before_frac, current_frac, d

            urls1, filenames1 = self.betweenPoints(PointA, PointB)
            urls += urls1
            filenames += filenames1

            loc = self.DistinctLocations.pop()

            before_frac = current_frac
        self.DistinctLocations.append(loc)

        '''
        if ( d > -1 and d <= 2*min_allowed_distance):
            # 0-40 meters, normal behavior
            urls, filenames = self.betweenPoints(self.Start, self.End)

        elif ( d > 2*min_allowed_distance and d <= 3*min_allowed_distance):
            # 40-60 meters, split into two
            Mid = midpoint(self.Start, self.End)
            urls1, filenames1 = self.betweenPoints(self.Start, Mid)
            self.DistinctLocations.pop()
            urls2, filenames2 = self.betweenPoints(Mid, self.End)
            urls = urls1 + urls2
            filenames = filenames1 + filenames2

        elif ( d > 3*min_allowed_distance and d <= 4*min_allowed_distance):
            # 60-80 meters, split into three
            Third1 = interpolation(self.Start, self.End, fraction=0.333)
            Third2 = interpolation(self.Start, self.End, fraction=0.666)
            urls1, filenames1 = self.betweenPoints(self.Start, Third1)
            self.DistinctLocations.pop()
            urls2, filenames2 = self.betweenPoints(Third1, Third2)
            self.DistinctLocations.pop()
            urls3, filenames3 = self.betweenPoints(Third2, self.End)
            urls = urls1 + urls2 + urls3
            filenames = filenames1 + filenames2 + filenames3

        elif ( d > 4*min_allowed_distance and d <= 5*min_allowed_distance):
            # 80-100 meters, split into four
            Mid = midpoint(self.Start, self.End)
            Quarter1 = midpoint(self.Start, Mid)
            Quarter2 = midpoint(Mid, self.End)
            urls1, filenames1 = self.betweenPoints(self.Start, Quarter1)
            self.DistinctLocations.pop()
            urls2, filenames2 = self.betweenPoints(Quarter1, Mid)
            self.DistinctLocations.pop()
            urls3, filenames3 = self.betweenPoints(Mid, Quarter2)
            self.DistinctLocations.pop()
            urls4, filenames4 = self.betweenPoints(Quarter2, self.End)
            urls = urls1 + urls2 + urls3 + urls4
            filenames = filenames1 + filenames2 + filenames3 + filenames4
        else:
            # 100 and more, split into five
            Fifth1 = interpolation(self.Start, self.End, fraction=0.2)
            Fifth2 = interpolation(self.Start, self.End, fraction=0.4)
            Fifth3 = interpolation(self.Start, self.End, fraction=0.6)
            Fifth4 = interpolation(self.Start, self.End, fraction=0.8)

            urls1, filenames1 = self.betweenPoints(self.Start, Fifth1)
            self.DistinctLocations.pop()
            urls2, filenames2 = self.betweenPoints(Fifth1, Fifth2)
            self.DistinctLocations.pop()
            urls3, filenames3 = self.betweenPoints(Fifth2, Fifth3)
            self.DistinctLocations.pop()
            urls4, filenames4 = self.betweenPoints(Fifth3, Fifth4)
            self.DistinctLocations.pop()
            urls5, filenames5 = self.betweenPoints(Fifth4, self.End)
            urls = urls1 + urls2 + urls3 + urls4 + urls5
            filenames = filenames1 + filenames2 + filenames3 + filenames4 + filenames5
        '''

        number_of_images = len(urls)
        self.resetImageMemory(number_of_images)


        for distLoc in self.DistinctLocations:
            self.DistinctNearbyVector.append(None)

        '''
        # DEBUG distances
        str_distances = ''
        last = self.DistinctLocations[0]
        for distLoc in self.DistinctLocations[1:]:
            d = 1000*distance_between_two_points(last, distLoc)
            last = distLoc
            str_distances += str(d)+', '
        print str_distances, self.DistinctLocations, self.LocationsIndex
        '''

        return [urls, filenames]
