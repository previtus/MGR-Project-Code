# Helper functions which tests the functionality of this block.


def testConnection():
    from OSMHandler.ConnectionHandlerObj import ConnectionHandler
    conHand = ConnectionHandler()
    [vec_a, _] = conHand.query_location(location=[14.4310467875143, 50.0631591705215], radius=10)
    [vec_b, _] = conHand.query_location(location=[14.4310467875143, 50.0631591705215], radius=100)

    print len(vec_a), vec_a
    print len(vec_b), vec_b


def testCheckingSegments():
    import OSMHandler.Checker as Checker
    import OSMHandler.Marker as Marker
    import Downloader.DataOperations

    #path_to_segments_file = '/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/StreetViewData/50_rewritingObj_299x299/SegmentsData.dump'
    #path_to_segments_file = '/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/StreetViewData/50_rewritingObj_299x299/SegmentsData_marked.dump'
    path_to_segments_file = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/1200x_markable_640x640/SegmentsData.dump'
    Segments = Downloader.DataOperations.LoadDataFile(path_to_segments_file)

    #Segments = Segments[0:3]
    radius = 100

    allright = Checker.Check(Segments)
    print "checks out as ", allright
    if not allright:
        Marker.Mark(Segments, radius = radius)

        Marker.closeConnection()

    allright = Checker.Check(Segments)
    print "checks out as ", allright

    path2 = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/1200x_markable_640x640/SegmentsData_marked_R100.dump'
    Segments = Downloader.DataOperations.SaveDataFile(path2, Segments)


testCheckingSegments()
