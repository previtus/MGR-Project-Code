import json
from Omnipresent import len_

def loadGeoJson(path):
    with open(path) as f:
        GeoJSON = json.load(f)
    return GeoJSON

def saveGeoJson(GeoJSON, path):
    print "Saving GeoJSON object to:", path
    with open(path, 'a') as f:
        json.dump(GeoJSON, f)

def loadDefaultGEOJSON():
    from DatasetHandler.FileHelperFunc import get_geojson_path
    path = get_geojson_path()
    return loadGeoJson(path)

def internalToExternal(score):
    if score <> -1:
        return int(round(score * 100))
    return score

def tmpMarkGeoJSON(GeoJSON, Segments):
    SegmentId = 0
    for feature in GeoJSON['features']:
        if (feature['geometry']['type'] == 'LineString'):
            json_score = feature['properties']['attractivity']
            internal_score = Segments[SegmentId].getScore()
            segments_score = internalToExternal(internal_score)

            if json_score == -1:
                feature['properties']['attractivity'] = 200

            SegmentId += 1

    return GeoJSON

def traverseGeoJSON(GeoJSON, Segments):
    SegmentId = 0
    for feature in GeoJSON['features']:
        if (feature['geometry']['type'] == 'LineString'):
            json_score = feature['properties']['attractivity']
            internal_score = Segments[SegmentId].getScore()
            segments_score = internalToExternal(internal_score)

            if json_score <> segments_score:
                print SegmentId, json_score, segments_score

            Coordinates = feature['geometry']['coordinates']
            Start = tuple([Coordinates[0][1], Coordinates[0][0]])
            End = tuple([Coordinates[-1][1], Coordinates[-1][0]])

            #segment = SegmentObj(Start, End, Score, SegmentId)
            #if verbose: segment.displaySegment()
            SegmentId += 1


GeoJSON = loadDefaultGEOJSON()
print GeoJSON.keys()

folder = '/home/ekmek/Vitek/MGR-Project-Code/Data/StreetViewData/'
path_to_segments_file = folder + '5556x_minlen30_640px/SegmentsData_marked_R100_4Tables.dump'

import Downloader.DataOperations as DataOperations
Segments = DataOperations.LoadDataFile(path_to_segments_file)

traverseGeoJSON(GeoJSON, Segments)


evaluated_geojson = tmpMarkGeoJSON(GeoJSON, Segments)
path_geojson_out = 'temp.geojson'
saveGeoJson(evaluated_geojson, path_geojson_out)

#traverseGeoJSON(a, Segments)
