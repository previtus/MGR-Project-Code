# GenerateGIFAnimation.py
import imageio

def GenerateGIFAnimation(Segments, GIFFileName):
    '''
    Create GIF animation from Segments.
    '''
    
    frames = 0
    with imageio.get_writer(GIFFileName, mode='I') as writer:
        for segment in Segments:
            if (segment.HasLoadedImage[0]):
                filename = segment.getImageFilename()
                #for fileTuple in FilenameMap:
                #filename = fileTuple[1]
                image = imageio.imread(filename)
                writer.append_data(image)
                frames += 1

    print "Saved to animation.gif with <", frames, "> frames."


    return []
