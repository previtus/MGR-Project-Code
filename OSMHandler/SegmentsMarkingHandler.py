# Helper functions which tests the functionality of this block.


def testConnection():
    # Test connection
    from OSMHandler.ConnectionHandlerObj import ConnectionHandler
    conHand = ConnectionHandler()
    [vec_a, _] = conHand.query_location(location=[14.4310467875143, 50.0631591705215], radius=10)
    [vec_b, _] = conHand.query_location(location=[14.4310467875143, 50.0631591705215], radius=100)

    print len(vec_a), vec_a
    print len(vec_b), vec_b


def markSegmentsWithRadius(input_path, output_path, radius = 100, close=False, interval=None):
    '''
    Mark these Segments with OSM data of said radius.
    :param input_path: path to initial Segments file (without any osm data)
    :param output_path: output where we want to save marked Segments
    :param radius: radius in meters.
    :param close: Flag to close connection after being done.
    :return:
    '''
    import OSMHandler.Checker as Checker
    import OSMHandler.Marker as Marker
    import Downloader.DataOperations

    Segments = Downloader.DataOperations.LoadDataFile(input_path)

    #allright = Checker.Check(Segments)
    allright = False
    print "checks out as ", allright
    if not allright:
        Marker.Mark(Segments, radius = radius, interval = interval)

        if close:
            Marker.closeConnection()

    allright = Checker.Check(Segments)
    print "checks out as ", allright

    Segments = Downloader.DataOperations.SaveDataFile(output_path, Segments)

"""
path = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/5556x_minlen30_640px_expanded/'
input_path = path+'SegmentsData_images_generated_2flipshift_expanded.dump'
output_path = path+'SegmentsData_mark100_images_generated_2flipshift_expanded.dump'
r = 100
markSegmentsWithRadius(input_path, output_path, radius = r, close=False)

input_path = path+'SegmentsData_images_generated_2flipshift_expanded.dump'
output_path = path+'SegmentsData_mark200_images_generated_2flipshift_expanded.dump'
r = 200
markSegmentsWithRadius(input_path, output_path, radius = r, close=False)

input_path = path+'SegmentsData_images_generated_2flipshift_expanded.dump'
output_path = path+'SegmentsData_mark50_images_generated_2flipshift_expanded.dump'
r = 50
markSegmentsWithRadius(input_path, output_path, radius = r, close=False)
"""

"""
path = '/home/ekmek/Project II/MGR-Project-Code/Data/StreetViewData/Prague_DOP_Cyklotrasy_l/'
input_path = path + 'SegmentsData_mark100_progress_1000-1100.dump'
output_path = path+'SegmentsData_mark100_progress_1000-1100.dump'
r = 100
markSegmentsWithRadius(input_path, output_path, radius = r, close=False, interval=[1000,1100])
"""

path = '/home/ekmek/Project II/MGR-Project-Code/Data/StreetViewData/Prague_DOP_Cyklotrasy_l/'
input_path = path + 'SegmentsData_mark100_progress_1100-1200.dump'
output_path = path+'SegmentsData_mark100_progress_1100-1200.dump'
r = 100
markSegmentsWithRadius(input_path, output_path, radius = r, close=False, interval=[1100,1200])
