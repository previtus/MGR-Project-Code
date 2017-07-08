# Functions.py
from math import *

import sys
sys.path.append('..')
from Downloader.Defaults import FromEdgeID
from DatasetHandler.FileHelperFunc import get_project_folder

def getApi():
    # Get secret Google Street View api code.
    api = open(get_project_folder()+'apicode.txt', 'r').read()
    return api

def bearing_between_two_points(start, end, degrees_offset=0.0):
    '''
    Calculates the initial bearing between two geographical locations.
    see: http://www.movable-type.co.uk/scripts/latlong.html
    The bearing is angular distance from NORTH.
    '''
    if (type(start) != tuple) or (type(end) != tuple):
        print type(start)
        raise TypeError("Function bearing_between_two_points takes only tuples.")
    
    lat1 = radians(start[0])
    lat2 = radians(end[0])
    dLong = radians(end[1] - start[1])
    
    x = sin(dLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - ( sin(lat1) * cos(lat2) * cos(dLong) )
    
    bearing = degrees( atan2(x,y) )

    bearing = bearing + degrees_offset

    bearing_from_north = (bearing + 360) % 360

    return bearing_from_north

def distance_between_two_points(start, end):
    '''
    Calculate distance between start and end
    :param start:
    :param end:
    :return: the distance
    '''
    lat1 = start[0]
    lat2 = end[0]
    lon1 = start[1]
    lon2 = end[1]

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def midpoint(start, end):
    '''
    Interpolate a midpoint between two points.
    :param start:
    :param end:
    :return: lat and lot of new point
    '''
    lat1 = start[0]
    lat2 = end[0]
    lon1 = start[1]
    lon2 = end[1]
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))

    Bx = cos(lat2) * cos(lon2 - lon1)
    By = cos(lat2) * sin(lon2 - lon1)

    lat3 = atan2(sin(lat1) + sin(lat2), sqrt((cos(lat1)+Bx)*(cos(lat1)+Bx) + By*By))
    lon3 = lon1 + atan2(By, cos(lat1) + Bx)

    return tuple(map(degrees, ([lat3, lon3])))


def interpolation(start, end, fraction):
    '''
    Interpolate a custom fraction between points.
    :param start:
    :param end:
    :param fraction: from 0 to 1
    :return:
    '''
    lat1 = start[0]
    lat2 = end[0]
    lon1 = start[1]
    lon2 = end[1]
    lat1, lon1, lat2, lon2 = map(radians, (lat1, lon1, lat2, lon2))

    sinlat1 = sin(lat1)
    coslat1 = cos(lat1)
    sinlon1 = sin(lon1)
    coslon1 = cos(lon1)
    sinlat2 = sin(lat2)
    coslat2 = cos(lat2)
    sinlon2 = sin(lon2)
    coslon2 = cos(lon2)

    dlat = lat2 - lat1;
    dlon = lon2 - lon1;
    a = sin(dlat/2.0) * sin(dlat/2.0) + cos(lat1) * cos(lat2) * sin(dlon/2.0) * sin(dlon/2.0)
    dd = 2.0 * atan2(sqrt(a), sqrt(1.0-a))

    A = sin((1.0-fraction)*dd) / sin(dd)
    B = sin(fraction*dd) / sin(dd)

    x = A * coslat1 * coslon1 + B * coslat2 * coslon2
    y = A * coslat1 * sinlon1 + B * coslat2 * sinlon2
    z = A * sinlat1 + B * sinlat2

    lat3 = atan2(z, sqrt(x*x + y*y))
    lon3 = atan2(y, x)

    return tuple(map(degrees, ([lat3, lon3])))

def segmentIDtoListID(semgentId):
    '''
    segment id might be 1000 if we start there, but the list is indexing from 0
    '''
    return semgentId-FromEdgeID
