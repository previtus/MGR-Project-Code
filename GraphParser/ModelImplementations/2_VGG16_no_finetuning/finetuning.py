from VisualizeHistory import *
from KerasPreparation import *
from load_vgg16_model_with_top import load_vgg16_model_with_custom_top
import keras
import time

# INPUTS
LocalFolder = ''

vgg16_weights_path = '/home/ekmek/TEMP_SPACE/vgg16/vgg16_weights.h5'
Folder = '../../1100downloaded_vII/'
path_to_segments_file = Folder+'SegmentsData.dump'

# OUTPUTS
target_folder = LocalFolder+'data/'

# SETTINGS
img_width, img_height = 150, 150


nb_epoch = 50

path_to_custom_top = '/home/ekmek/TEMP_SPACE/MGR-Project-Code/GraphParser/ModelImplementations/2_VGG16_no_finetuning/now1/data/top_model_weights.h5'
model = load_vgg16_model_with_custom_top(path_to_custom_top)


# Now to run the model
[x, y, x_val, y_val] = Prepare_DataLabels_withGeneratedData(path_to_segments_file,img_width, img_height,validation_split=0.25,path_to_images=Folder,shuffle_=False,seed_=42,
                                                            target_number_of_trainset=2000, target_number_of_validset=None)
now = time.strftime("%c")
log1 = keras.callbacks.TensorBoard(log_dir=LocalFolder+'data/'+now, histogram_freq=1, write_graph=False, write_images=False)
log2 = keras.callbacks.CSVLogger(LocalFolder+'data/logCSV.csv', separator=',', append=False)
#logcalls = [log1, log2]
logcalls = []

history = model.fit(x, np.array(y),
        nb_epoch=nb_epoch, batch_size=32,
        validation_data=(x_val, np.array(y_val)), callbacks=logcalls
)

# I hope it saves the whole model and not just the VGG16 segments
model.save_weights(target_folder + 'whole_finetuned_model_weights.h5')
model.save(target_folder + 'whole_finetuned_model.h5')

saveHistory(history.history, LocalFolder + 'results/history_finetune.npy')
visualize_history(history.history, save=True, save_path=LocalFolder + 'results/finetune_' + str(nb_epoch))

# LOL 1984/2000 [============================>.] - ETA: 11s - loss: 0.0182 - mean_squared_logarithmic_error: 0.0086terminate called after throwing an instance of 'std::bad_alloc'
#  what():  std::bad_alloc
# 1984/2000 [============================>.] - ETA: 7s - loss: 0.0176 - mean_squared_logarithmic_error: 0.0084 terminate called after throwing an instance of 'std::bad_alloc'
#  what():  std::bad_alloc
# 1000 toooo