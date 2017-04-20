# Helper functions which tests the functionality of this block.


def testConnection():
    from OSMHandler.ConnectionHandlerObj import ConnectionHandler
    conHand = ConnectionHandler()
    conHand.query_location(location=[])

def testCheckingSegments():
    import OSMHandler.Checker as Checker
    import OSMHandler.Marker as Marker
    import Downloader.DataOperations

    path_to_segments_file = '/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/StreetViewData/50_rewritingObj_299x299/SegmentsData.dump'
    Segments = Downloader.DataOperations.LoadDataFile(path_to_segments_file)

    Segments = Segments[0:3]

    allright = Checker.Check(Segments)
    if not allright:
        Marker.Mark(Segments)

    Marker.closeConnection()

    allright = Checker.Check(Segments)


testConnection()
