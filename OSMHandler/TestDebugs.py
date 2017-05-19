# Helper functions which tests the functionality of this block.


def testConnection():
    from OSMHandler.ConnectionHandlerObj import ConnectionHandler
    conHand = ConnectionHandler()
    [vec_a, _] = conHand.query_location(location=[14.4310467875143, 50.0631591705215], radius=10)
    [vec_b, _] = conHand.query_location(location=[14.4310467875143, 50.0631591705215], radius=100)

    print len(vec_a), vec_a
    print len(vec_b), vec_b


def testCheckingSegments(input_path, output_path):
    import OSMHandler.Checker as Checker
    import OSMHandler.Marker as Marker
    import Downloader.DataOperations

    #path_to_segments_file = '/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/StreetViewData/50_rewritingObj_299x299/SegmentsData.dump'
    #path_to_segments_file = '/home/ekmek/Desktop/Project II/MGR-Project-Code/Data/StreetViewData/50_rewritingObj_299x299/SegmentsData_marked.dump'
    #path_to_segments_file = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_markable_640x640/SegmentsData.dump'
    Segments = Downloader.DataOperations.LoadDataFile(input_path)

    #Segments = Segments[0:3]
    radius = 100

    allright = Checker.Check(Segments)
    print "checks out as ", allright
    if not allright:
        Marker.Mark(Segments, radius = radius)

        Marker.closeConnection()

    allright = Checker.Check(Segments)
    print "checks out as ", allright

    Segments = Downloader.DataOperations.SaveDataFile(output_path, Segments)


input_path = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/1200x_markable_299x299/SegmentsData.dump'
output_path = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/1200x_markable_299x299/SegmentsData_marked_R100_4Tables.dump'
testCheckingSegments(input_path, output_path)

input_path = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_markable_640x640/SegmentsData.dump'
output_path = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_markable_640x640/SegmentsData_marked_R100_4Tables.dump'
testCheckingSegments(input_path, output_path)

