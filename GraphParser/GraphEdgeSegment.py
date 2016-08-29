from Functions import *


class GraphEdgeSegment:
    'Common base class for all employees'
    tmp = 0
    
    def __init__(self, FromId, ToId, Nodes):
        self.FromId = FromId
        self.ToId = ToId

        # Latitude,Latitude projected,Longitude,Longitude projected,Elevation
        #self.Start = map(float, Nodes[FromId])
        #self.End = map(float, Nodes[ToId])
        self.Start = ( float(Nodes[FromId][0]), float(Nodes[FromId][2]) )
        self.End = ( float(Nodes[ToId][0]), float(Nodes[ToId][2]) )

        self.ProjectedStart = ( float(Nodes[FromId][1]), float(Nodes[FromId][3]) )
        self.ProjectedEnd = ( float(Nodes[ToId][1]), float(Nodes[ToId][3]) )
        
        self.ElevationStart = float(Nodes[FromId][4])
        self.ElevationEnd = float(Nodes[ToId][4])
        
        GraphEdgeSegment.tmp += 1
   
    def displaySegment(self):
        print "From: ", self.FromId,  ", To: ", self.ToId
        print "Start: ", self.Start
        print "End: ", self.End

    def getBearingString(self):
        return bearing_between_two_points(self.Start, self.End)

    def getGoogleViewUrl(self):
        'Google View url from the start of this segment'
        # http://maps.googleapis.com/maps/api/
        # streetview?size=600x400&location=<lat>,<long>&heading=<angle from north>&key=<api>
        lat = self.Start[0]
        lon = self.Start[1]
        bearing = round(self.getBearingString(), 2)
        url_start = "http://maps.googleapis.com/maps/api/streetview?size=600x400&location="
        api = getApi()
        
        full_url = [url_start, str(lat), ",", str(lon), "&heading=", str(bearing), "&key=", api]

        return "".join(full_url)
