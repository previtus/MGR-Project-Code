import urllib2
from multiprocessing import Pool

def job(url_tuple):
    url = url_tuple[0]
    file_name = url_tuple[1]
    print url
    print file_name
    '''
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    f.write(u.read())
    f.close()
    '''

pool = Pool()

url1 = "http://maps.googleapis.com/maps/api/streetview?size=600x400&location=50.045253,14.42553&heading=268.97&key=AIzaSyAUa8vWg3uhyrJTM3qq7zMQTj562bN608A"
url2 = "http://maps.googleapis.com/maps/api/streetview?size=600x400&location=50.045254,14.42453&heading=268.97&key=AIzaSyAUa8vWg3uhyrJTM3qq7zMQTj562bN608A"

#job(url,name)
urls = [(url1, "aaa.jpg"), (url2, "bbb.jpg")]

#map(job, urls)
pool.map(job, urls)

# !!! is unsuccessful
