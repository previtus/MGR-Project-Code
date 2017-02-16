import numpy as np
from scipy.misc import imread, imresize, imsave

# Helper functions for loading of images

def list_images(folder):

    # prepare list of image names
    from os import listdir
    from os.path import isfile, join
    image_list = [folder + f for f in listdir(folder) if isfile(join(folder, f))]
    return image_list

def len_(L):
    return np.array(L).shape

def preprocess_image_batch(image_paths, img_size=None, crop_size=None, color_mode="rgb", out=None):
    img_list = []

    for im_path in image_paths:
        img = imread(im_path, mode='RGB')
        if img_size:
            try:
                img = imresize(img,img_size)
            except:
                print 'failed resizing image', im_path
                raise
        img = img.astype('float32')
        # We normalize the colors (in RGB space) with the empirical means on the training set
        img[:, :, 0] -= 123.68
        img[:, :, 1] -= 116.779
        img[:, :, 2] -= 103.939
        # We permute the colors to get them in the BGR order
        if color_mode=="bgr":
            img[:,:,[0,1,2]] = img[:,:,[2,1,0]]
        img = img.transpose((2, 0, 1))

        if crop_size:
            img = img[:,(img_size[0]-crop_size[0])//2:(img_size[0]+crop_size[0])//2
                      ,(img_size[1]-crop_size[1])//2:(img_size[1]+crop_size[1])//2]

        img_list.append(img)

    try:
        img_batch = np.stack(img_list, axis=0)
    except:
        raise ValueError('when img_size and crop_size are None, images'
                ' in image_paths must have the same shapes.')

    if out is not None and hasattr(out, 'append'):
        out.append(img_batch)
    else:
        return img_batch

def saveArrayToCSV(array,filename):
    a = np.asarray(array)
    np.savetxt(filename, a, delimiter=",")
