# Functions.py
from math import *

import sys
sys.path.append('..')
from Downloader.Defaults import FromEdgeID
from DatasetHandler.FileHelperFunc import get_project_folder

def getApi():
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

def segmentIDtoListID(semgentId):
    '''
    segment id might be 1000 if we start there, but the list is indexing from 0
    '''
    return semgentId-FromEdgeID
