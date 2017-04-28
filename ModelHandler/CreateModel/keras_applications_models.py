from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.resnet50 import ResNet50
from keras.applications.inception_v3 import InceptionV3
from keras.applications.xception import Xception


def vgg16():
    model = VGG16(weights='imagenet', include_top=False)
    print('VGG16 partial model loaded.')
    return model

def vgg19():
    model = VGG19(weights='imagenet', include_top=False)
    print('VGG19 partial model loaded.')
    return model

def resnet50():
    model = ResNet50(weights='imagenet', include_top=False)
    print('ResNet50 partial model loaded.')
    return model

def inception_v3():
    model = InceptionV3(weights='imagenet', include_top=False)
    print('InceptionV3 partial model loaded.')
    return model

def xception():
    model = Xception(weights='imagenet', include_top=False)
    print('Xception (TensorFlow only) partial model loaded.')
    return model

def all_models():
    #return [['vgg16', vgg16()]]
    return [['vgg16', vgg16()], ['vgg19', vgg19()], ['resnet50', resnet50()],
            ['inception_v3', inception_v3()], ['xception', xception()]]

def load_model(name="vgg16"):
    if name == "vgg16":
        return vgg16()
