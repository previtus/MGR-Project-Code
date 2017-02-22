# GenerateGIFAnimation.py
import imageio

def GenerateGIFAnimation(Segments, GIFFileName):
    '''
    Create GIF animation from Segments.
    '''
    
    frames = 0
    with imageio.get_writer(GIFFileName, mode='I') as writer:
        # there
        for segment in Segments:
            if (segment.HasLoadedImages[0]):
                filename = segment.getImageFilename(0)
                #for fileTuple in FilenameMap:
                #filename = fileTuple[1]
                image = imageio.imread(filename)
                writer.append_data(image)
                frames += 1
        # and back
        for segment in Segments:
            if (segment.HasLoadedImages[1]):
                filename = segment.getImageFilename(1)
                #for fileTuple in FilenameMap:
                #filename = fileTuple[1]
                image = imageio.imread(filename)
                writer.append_data(image)
                frames += 1


    print "Saved to", GIFFileName, "with <", frames, "> frames."


    return []
