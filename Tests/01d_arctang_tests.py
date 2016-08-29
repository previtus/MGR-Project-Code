from math import *
from fce01d_bearing import *

# Latitude,Latitude projected,Longitude,Longitude projected,Elevation
# A: 50.072025,1044545.0,14.404032,744265.0,199.0
# B: 50.072067,1044542.0,14.404188,744253.0,200.0

lat1 = 50.072025
long1 = 14.404032
lat2 = 50.072067
long2 = 14.404188

plat1 = 1044545
plong1 = 744265
plat2 = 1044542
plong2 = 744253

pointA = (lat1, long1)
pointB = (lat2, long2)

print bearing_between_two_points(pointA, pointB)
