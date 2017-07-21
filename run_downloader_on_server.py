from Downloader.DownloaderRunner import RunDownload, RunCheck, RunMarkBad
import sys

name = "DatasetName"
from_id = 0
to_id = 5556 #5556
pixels = 640
minimal_length = 10
custom_geojson = ''

# python run_downloader_on_server.py NAME FROMID TOID PIXELS MIN_LEN
if len(sys.argv) > 4:
    name = sys.argv[1]  # var1
    from_id = int(sys.argv[2])  # var2
    to_id = int(sys.argv[3])  # var3
    pixels = int(sys.argv[4])  # var4
    minimal_length = int(sys.argv[5])  # var5
else:
    print "Using default values. Please run as: run_downloader_on_server.py nameOfFolder fromId toId pixels minimalLength"

print "[Setting] run_downloader_on_server.py", name, from_id, to_id, pixels

print 'CAREFULLY CHECK THE FILE_NOT_FOUND_CHECKSUM!!! Is it the one for '+str(pixels)+' ??'

RunDownload(name, from_id, to_id, pixels, minimal_length, custom_geojson)
#RunCheck(name, pixels)
