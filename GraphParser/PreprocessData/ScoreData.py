# ScoreData.py
from PIL import Image
from PIL import *

# more fancy methods at: http://stackoverflow.com/questions/9018016/how-to-compare-two-colors

def distanceColors(col1, col2):
    '''
    input colors in list: [R, G, B]
    '''
    cR = col1[0]-col2[0] 
    cG = col1[1]-col2[2]
    cB = col1[2]-col2[2] 
    uR = col1[0]+col2[0]
    distance = cR*cR*(2+uR/256) + cG*cG*4 + cB*cB*(2+(255-uR)/256)
    return distance

def ScoreData(Segments):
    # Score segments by some measurement of route attractivity
    # inital temporary implemtation - score by the number of "green" pixels
    for Segment in Segments:
        # only "valid" segments
        if Segment.hasLoadedImage():
            image_name = Segment.getImageFilename()

            thresholt = 10000
            thresholt = 50000
            green = [0,255,0]
            greens = 0
            im = Image.open(image_name)
            num_pixels = len(im.getdata())

            for pixel in im.getdata():
                if distanceColors(list(pixel), green) < thresholt:
                    greens += 1

            score = float(greens) / num_pixels
            print image_name, ", green pixels: ", greens, "/", num_pixels, ", score: ", score

            Segment.Score = score


