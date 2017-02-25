import keras.applications as applications
from keras.preprocessing import image
from keras.models import Model
from keras.layers import Dense, Dropout, GlobalAveragePooling2D, Flatten
from keras import backend as K
import keras.utils.visualize_util as visualize_util
import numpy as np

input_shape=(299, 299, 3)
#base_model = applications.inception_v3.InceptionV3(weights='imagenet', include_top=True, input_shape=input_shape)
#base_model = applications.xception.Xception(include_top=True, weights='imagenet', input_tensor=None, input_shape=input_shape)

#visualize_util.plot(base_model, to_file='model_xception_withItsOriginalTop.png', show_shapes=True)

base_model = applications.xception.Xception(include_top=False, weights='imagenet', input_tensor=None, input_shape=input_shape)

#visualize_util.plot(base_model, to_file='model_xception_withoutTop.png', show_shapes=True)

#output = base_model.output
#print output
# NO TOP:
# input shape None: Tensor("concat_14:0", shape=(?, 2048, ?, ?), dtype=float32)
# input shape (3, 224, 224): shape=(?, 2048, 5, 5)


x = 0
x_val = 0
target_folder = '../../Data/ModelFiles/'
bottleneck_features_train = base_model.predict(x, verbose=1)
np.save(open(target_folder + 'Xception_features_train.npy', 'w'), bottleneck_features_train)
bottleneck_features_validation = base_model.predict(x_val, verbose=1)
np.save(open(target_folder + 'Xception_features_validation.npy', 'w'), bottleneck_features_validation)


'''
# Build custom top

x = base_model.output
x = GlobalAveragePooling2D()(x) # instead of Flatten?

x = Dense(1024, activation='relu')(x)
x = Dropout(0.5)(x)
output_score = Dense(1, activation='sigmoid')(x)

# this is the model we will train
model = Model(input=base_model.input, output=output_score)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='rmsprop', loss='mean_squared_error')
#model.compile(optimizer='adam', loss='mean_squared_error')

visualize_util.plot(model, to_file='TEST.png', show_shapes=True)

'''