import urllib

# saves into the folder of script
urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")

# doesn't save into the folder of script (apparently to temp folder)
data = urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000002.jpg")
