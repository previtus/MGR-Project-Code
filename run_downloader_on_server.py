from Downloader.DownloaderRunner import RunDownload, RunCheck
import sys

name = "5556x_markable_299x299"
from_id = 0
to_id = 5556
pixels = 299

# python python_script.py NAME FROMID TOID PIXELS
if len(sys.argv) > 4:
    name = sys.argv[1]  # var1
    from_id = int(sys.argv[2])  # var2
    to_id = int(sys.argv[3])  # var3
    pixels = int(sys.argv[4])  # var4
else:
    print "Using default values. Please run as: python_script.py nameOfFolder fromId toId pixels"

print "[Setting] python_script.py", name, from_id, to_id, pixels

RunDownload(name, from_id, to_id, pixels)
RunCheck(name, pixels)
