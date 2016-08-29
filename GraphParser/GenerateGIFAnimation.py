import imageio

def GenerateGIFAnimation(FilenameMap, GIFFileName):
    '''
    Create GIF animation from files mentioned in FilenameMap.
    List of tuples in [ (<url>, <filename>), ... ]
    uses only the <filename> section
    '''
    
    frames = 0
    with imageio.get_writer(GIFFileName, mode='I') as writer:
        for fileTuple in FilenameMap:
            filename = fileTuple[1]
            image = imageio.imread(filename)
            writer.append_data(image)
            frames += 1

    print "Saved to animation.gif with <", frames, "> frames."


    return []
