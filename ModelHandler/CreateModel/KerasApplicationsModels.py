from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from keras.applications.inception_v3 import InceptionV3
from keras.applications.xception import Xception


def vgg16(input_shape=None):
    model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    print 'VGG16 partial model loaded with input shape ', input_shape
    return model

def vgg19(input_shape=None):
    model = VGG19(weights='imagenet', include_top=False, input_shape=input_shape)
    print 'VGG19 partial model loaded with input shape ', input_shape
    return model

def resnet50(input_shape=None):
    model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    print 'ResNet50 partial model loaded with input shape ', input_shape
    return model

def inception_v3(input_shape=None):
    model = InceptionV3(weights='imagenet', include_top=False, input_shape=input_shape)
    print 'InceptionV3 partial model loaded with input shape ', input_shape
    return model

def xception(input_shape=None):
    model = Xception(weights='imagenet', include_top=False, input_shape=input_shape)
    print 'Xception (TensorFlow only) partial model loaded with input shape ', input_shape
    return model

#def all_models():
#    #return [['vgg16', vgg16()]]
#    return [['vgg16', vgg16()], ['vgg19', vgg19()], ['resnet50', resnet50()],
#            ['inception_v3', inception_v3()], ['xception', xception()]]

def all_model_names():
    #return [['vgg16', vgg16()]]
    return ['vgg16', 'vgg19', 'resnet50', 'inception_v3', 'xception']

def get_model(name, pixels=None):
    input_shape=None
    if pixels is not None:
        input_shape=(int(pixels), int(pixels), 3)

    if name == 'vgg16':
        return vgg16(input_shape)
    elif name == 'vgg19':
        return vgg19(input_shape)
    elif name == 'resnet50':
        return resnet50(input_shape)
    elif name == 'inception_v3':
        return inception_v3(input_shape)
    elif name == 'xception':
        return xception(input_shape)
