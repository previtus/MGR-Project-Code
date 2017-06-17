# Runs tests on Models - will perform all calls to Keras functions like fit, predics, etc. and produce history of the
# process.
# Takes models as inputs.
# Can run either simple tests, or the more complicated ones separeted into:
# - train top > finetune CNN > finetune everything
# Can perform the more precise k-fold cross validation

from ModelHandler.ModelGenerator import build_simple_top_model, build_full_mixed_model, build_finetune_model, join_two_models
from ModelHandler.KfoldTester import k_fold_crossvalidation
from Omnipresent import len_
import numpy as np
from keras.utils import plot_model
from Downloader.VisualizeHistory import saveHistory, visualize_history

def cook_features(models, datasets, Settings):
    '''
    Makes sure that we have features available for the duo of model-dataset in our shared feature folder.
    If not, we will cook them.
    :param models: list of models (currently without their tops)
    :param datasets: list of dataset object
    :param Settings: settings
    :return: number of ready models
    '''
    # cooking shared data
    [x, y, x_val, y_val] = [None, None, None, None]

    index = 0
    for model in models:
        model_settings = Settings["models"][index]

        # TODO: MODEL_TYPE_SPLIT

        if model_settings["model_type"] is 'simple_cnn_with_top' or model_settings["model_type"] is 'img_osm_mix':

            dataset = datasets[ model_settings["dataset_pointer"] ]
            from ModelHandler.ModelOI import get_feature_file_names, do_we_need_to_cook
            #ps: if this is in the header of the file, it causes mutual import of each other - and TF yells...

            filename_features_train = model_settings["filename_features_train"]
            filename_features_test = model_settings["filename_features_test"]
            do_we_need_to_cook_bool = do_we_need_to_cook(filename_features_train, filename_features_test)
            print "Looking up files:", filename_features_train, filename_features_test

            if do_we_need_to_cook_bool:
                model_cnn = model[0]
                cooking_method = model_settings["cooking_method"]

                print "We need to cook, chosen method is", cooking_method
                #if True:
                if cooking_method == 'direct':
                    if x is None:
                        [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=model_settings["validation_split"])
                        print len_(x)

                    predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model_cnn)

                #if True:
                elif cooking_method == 'generators':
                    [order, order_val, image_generator, size, image_generator_val, size_val] = dataset.getImageGenerator(validation_split=model_settings["validation_split"])
                    print len_(order)

                    predict_from_generators(image_generator, image_generator_val, size, size_val, filename_features_train, filename_features_test, model_cnn)
            else:
                print "No need to cook, the files already exist"

            # Finetuning also requires prepared feature files.
            if model_settings["finetune"]:
                finetune_features_train = model_settings["finetune_features_train"]
                finetune_features_test = model_settings["finetune_features_test"]
                do_we_need_to_cook_bool = do_we_need_to_cook(finetune_features_train, finetune_features_test)
                print "Looking up finetune feature files:", finetune_features_train, finetune_features_test

                if do_we_need_to_cook_bool:
                    model_cnn = model[0]
                    cooking_method = model_settings["cooking_method"]

                    #n = len(model[0].layers) - model_settings["finetune_num_of_cnn_layers"]
                    n = model_settings["finetune_num_of_cnn_layers"]

                    '''
                    for layer in model[0].layers[:n]:
                        print layer
                        #layer.trainable = False
                    print "----------------"
                    for layer in model[0].layers[n:]:
                        print layer
                    print model[0].layers[n]
                    '''

                    print "------ Omitting layers:"
                    for layer in model[0].layers[n:]:
                        print layer.get_config()['name'], layer

                    print "Saving this layers outputs:"
                    print model_cnn.layers[n].get_config()['name'], model_cnn.layers[n], model_cnn.layers[n].get_config()

                    from keras.models import Model
                    model_middle = Model(inputs=model_cnn.input, outputs=model_cnn.layers[n].output)

                    print "We need to for finetuning files too, chosen method is", cooking_method
                    if cooking_method == 'direct':
                        if x is None:
                            [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=model_settings["validation_split"])
                            print len_(x)
                        predict_and_save_features(x, y, x_val, y_val, finetune_features_train, finetune_features_test, model_middle)

                    elif cooking_method == 'generators':
                        [order, order_val, image_generator, size, image_generator_val, size_val] = dataset.getImageGenerator(validation_split=model_settings["validation_split"])
                        print len_(order)
                        predict_from_generators(image_generator, image_generator_val, size, size_val, finetune_features_train, finetune_features_test, model_middle)
                else:
                    print "No need to cook finetune feature files, they already exist"


        elif model_settings["model_type"] is 'osm_only':
            # No need to cook features from images in this case
            print "Chosen model type (", model_settings["model_type"] ,") doesn't require features to be cooked and loaded."
        index += 1
    return index

def train_models(models, datasets, Settings):
    '''
    Training on all models - dataset pairs from models.
    :param models: array of models to run
    :param dataset:
    :param Settings:
    :return:
    '''
    number_of_models = len(Settings["models"])
    print "## Testing",number_of_models,"models."

    histories = []
    index = 0
    for model in models:
        model_settings = Settings["models"][index]
        dataset = datasets[ model_settings["dataset_pointer"] ]

        if model_settings["k_fold_crossvalidation"]:
            print "k-fold crossvalidation testing, k=", model_settings["crossvalidation_k"], model_settings["unique_id"], model
            history = k_fold_crossvalidation(model, dataset, model_settings)
            histories.append(history) # SPECIAL HISTORY IN THIS CASE THOUGH

        else:
            print "Regular testing", model_settings["unique_id"], model
            history = train_model(model, dataset, model_settings)
            histories.append(history)

        index += 1
    return histories

def train_model(model, dataset, model_settings):
    history = None
    # TODO: MODEL_TYPE_SPLIT

    if model_settings["model_type"] is 'simple_cnn_with_top':

        filename_features_train = model_settings["filename_features_train"]
        filename_features_test = model_settings["filename_features_test"]

        [y, y_val] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])
        [train_data, train_labels, validation_data, validation_labels] = load_features(filename_features_train, filename_features_test, y, y_val)

        print "input shape of features", len_(train_data), "and labels", len_(train_labels)

        top_model = model[1]
        history = train_top_model(top_model, model_settings, train_data, train_labels, validation_data, validation_labels)

        # Finetuning
        print len_(history)
        print history

        if model_settings["finetune"]:
            finetune_model = None
            [train_data, train_labels, validation_data, validation_labels] = [None, None, None, None]

            # Cut at certain spots - only possible where Resnet50 structure allows it 172, 162, 152, 140, ...
            if model_settings["finetune_DEBUG_METHOD_OF_MODEL_GEN"]:
                finetune_features_train = model_settings["finetune_features_train"]
                finetune_features_test = model_settings["finetune_features_test"]

                [y, y_val] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])
                [train_data, train_labels, validation_data, validation_labels] = load_features(finetune_features_train, finetune_features_test, y, y_val)

                print "FINE TUNE DATA input shape of features", len_(train_data), "and labels", len_(train_labels)

                # Fce (top, cnn, features_mid) > new_model
                model_cnn = model[0]
                top_cnn = model[1]
                cut = model_settings["finetune_num_of_cnn_layers"]
                shape = np.asarray(train_data).shape[1:]
                print shape

                finetune_model = build_finetune_model(model_cnn, top_cnn, cut, input_shape=shape)
                print "----- finetune model"
                print finetune_model.summary()

                plot_model(finetune_model, to_file='TEST_FINETUNE.png', show_shapes=True)

                '''
                Total params: 5,128,193
                Trainable params: 5,122,049
                Non-trainable params: 6,144
                '''

            # Its possible to do it anywhere, but that will bring it lengthy evaluation here on the spot without cooking
            else:

                n = model_settings["finetune_num_of_cnn_layers"]

                for layer in model[0].layers[:n]:
                    print layer
                    layer.trainable = False

                print "----- CNN MODEL"
                print model[0].summary()
                print "----- TOP MODEL"
                print model[1].summary()

                # New model is made from the cnn and top model
                finetune_model = join_two_models(model[0], model[1])

                print "----- JOINED MODEL"
                print finetune_model.summary()

                plot_model(finetune_model, to_file='TEST_MODEL.png', show_shapes=True)

                [train_data, train_labels, validation_data, validation_labels] = dataset.getDataLabels_split(validation_split=model_settings["validation_split"])

                '''
                Total params: 24,244,097
                Trainable params: 5,122,049
                Non-trainable params: 19,122,048
                '''
            # We have the model, now lets compute

            epochs_tmp = model_settings["epochs"]
            model_settings["epochs"] = model_settings["finetune_epochs"]
            optimizer_tmp = model_settings["optimizer"]
            model_settings["optimizer"] = model_settings["finetune_optimizer"]


            history_to_append = train_top_model(finetune_model, model_settings, train_data, train_labels, validation_data, validation_labels)
            model_settings["epochs"] = epochs_tmp
            model_settings["optimizer"] = optimizer_tmp

        # Append histories

        #{'val_mean_absolute_error': [0.27633494684393978, 0.27673623693381116], 'loss': [0.15686354677721928, 0.12237877659907737], 'mean_absolute_error': [0.3303849070751238, 0.30686430593424935], 'val_loss': [0.10361090554317957, 0.10128958691173875]}
        if model_settings["finetune"]:
            print history
            print history_to_append
            for key in history.keys():
                history[key] += history_to_append[key]
            print history


    elif model_settings["model_type"] is 'img_osm_mix':

        if (model_settings["special_case"] is 'hack_dont_use_features'):
            # 0 Get data
            # ps: be careful about their order when enhancing...
            # ImageGenerator for multiple inputs
            # check - https://github.com/fchollet/keras/issues/3386
            # >> DatasetObj >> generator_triple_with_enhancement

            # 1 Build whole model now
            osm_shape = dataset.getShapeOfOsm()
            model = build_full_mixed_model(osm_shape)

            # 2 Train (which will take some time now...)
            [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=model_settings["validation_split"])
            [osm, osm_val] = dataset.getDataLabels_split_only_osm(validation_split=model_settings["validation_split"])

            history = train_top_model(model, model_settings, [x, osm], y, [x_val, osm_val], y_val)

            print "foo"
        else:

            filename_features_train = model_settings["filename_features_train"]
            filename_features_test = model_settings["filename_features_test"]

            [osm, osm_val] = dataset.getDataLabels_split_only_osm(validation_split=model_settings["validation_split"])
            [y, y_val] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])
            [train_data, _, validation_data, _] = load_features(filename_features_train, filename_features_test, y, y_val)

            print len_(train_data), len_(y), len_(osm)

            top_model = model[1]
            history = train_top_model(top_model, model_settings, [osm, train_data], y, [osm_val, validation_data], y_val)

    elif model_settings["model_type"] is 'osm_only':

        [osm, osm_val] = dataset.getDataLabels_split_only_osm(validation_split=model_settings["validation_split"])
        [y, y_val] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])

        #if model_settings["intermix"]:
        #    [osm, y, osm_val, y_val] = dataset.mix_within_groups([osm, y], [osm_val, y_val], model_settings["seed"])

        osm_model = model[0]
        history = train_top_model(osm_model, model_settings, osm, y, osm_val, y_val)

    else:
        print "Yet to be programmed."

    return history

# Generate Feature files = Predict
def predict_from_generators(test_generator, val_generator, number_in_test, number_in_val, filename_features_train, filename_features_test, model):
    # generators should yield:
    bottleneck_features_train = model.predict_generator(test_generator, steps=number_in_test,verbose=1)
    print "saving train_features of size", len_(bottleneck_features_train), " into ",filename_features_train
    np.save(open(filename_features_train, 'w'), bottleneck_features_train)
    bottleneck_features_validation = model.predict_generator(val_generator, steps=number_in_val,verbose=1)
    print "saving val_features of size", len_(bottleneck_features_validation), " into ",filename_features_test
    np.save(open(filename_features_test, 'w'), bottleneck_features_validation)

def predict_and_save_features(x, y, x_val, y_val, filename_features_train, filename_features_test, model):
    # dimensions of x are (num,3,x_dim, y_dim) = (75, 3, 150, 150)
    bottleneck_features_train = model.predict(x,verbose=1)
    np.save(open(filename_features_train, 'w'), bottleneck_features_train)
    print "saving train_features of size", len_(bottleneck_features_train), " into ",filename_features_train
    bottleneck_features_validation = model.predict(x_val,verbose=1)
    print "saving val_features of size", len_(bottleneck_features_validation), " into ",filename_features_test
    np.save(open(filename_features_test, 'w'), bottleneck_features_validation)

def load_features(filename_features_train, filename_features_test, y, y_val):
    train_data = np.load(open(filename_features_train))
    train_labels = np.array(y)

    validation_data = np.load(open(filename_features_test))
    validation_labels = np.array(y_val)
    return [train_data, train_labels, validation_data, validation_labels]

def load_feature_file(path):
    '''
    Just loads the features stored in one file.
    :param path:
    :return:
    '''
    try:
        data = np.load(open(path))
        return data
    except:
        print "Failed to load file", path
        return 0

# Test Whole model = Fit
def train_top_model(model, model_settings, train_data, train_labels, validation_data, validation_labels):
    if len(train_data) <> 2:
        train_data = np.array(train_data)
        validation_data = np.array(validation_data)
    else:
        train_data[0] = np.array(train_data[0])
        train_data[1] = np.array(train_data[1])
        validation_data[0] = np.array(validation_data[0])
        validation_data[1] = np.array(validation_data[1])
    train_labels = np.array(train_labels)
    validation_labels = np.array(validation_labels)

    model.compile(optimizer=model_settings["optimizer"], loss=model_settings["loss_func"], metrics=model_settings["metrics"])

    history = model.fit(train_data, train_labels, verbose=1,
              epochs=model_settings["epochs"], batch_size=32,
              validation_data=(validation_data, validation_labels))

    #history = model.fit_generator(generator_train, steps_per_epoch, epochs=epochs,
    #                              validation_data=(generator_valid), validation_steps)

    return history.history


# CUSTOM KERAS CALLBACK
# inspired by Kerutils at https://github.com/samyzaf/kerutils
from keras.callbacks import Callback
import datetime, sys

def format_time(seconds):
    if seconds < 400:
        s = float(seconds)
        return "%.1f seconds" % (s,)
    elif seconds < 4000:
        m = seconds / 60.0
        return "%.2f minutes" % (m,)
    else:
        h = seconds / 3600.0
        return "%.2f hours" % (h,)

class RunMonitor(Callback):
    def __init__(self, **opt):
        super(Callback, self).__init__()
        self.verbose = opt.get('verbose', 1)
        self.hist = {'loss': [], 'val_loss': []}
        self.current_epoch = -1

    def on_epoch_begin(self, epoch, logs={}):
        self.current_epoch = epoch

    def on_train_begin(self, logs={}):
        self.start_time = datetime.datetime.now()
        t = datetime.datetime.strftime(self.start_time, '%Y-%m-%d %H:%M:%S')
        print "Training started:", t

        self.progress = 0

    def on_train_end(self, logs={}):
        self.end_time = datetime.datetime.now()
        t = datetime.datetime.strftime(self.end_time, '%Y-%m-%d %H:%M:%S')
        time_str = format_time(self.end_time - self.start_time)
        print "Training ended:", t, "(took ", time_str, ")"

    #def on_batch_end(self, batch, logs={}):

    def on_epoch_end(self, epoch, logs={}):
        loss = logs.get('loss')
        val_loss = logs.get('val_loss', -1)

        percentage = int(epoch / (self.params['epochs'] / 100.0))
        if percentage > self.progress:
            sys.stdout.write('.')
            if percentage%5 == 0:
                dt = datetime.datetime.now() - self.start_time
                time_str = format_time(dt.total_seconds())
                fmt = '%02d%% epoch=%d, loss=%f, val_loss=%f, time=%s\n'
                vals = (percentage,    epoch,    loss,    val_loss,    time_str)

                sys.stdout.write(fmt % vals)
            sys.stdout.flush()
            self.progress = percentage

    def print_params(self):
        for key in sorted(self.params.keys()):
            print("%s = %s" % (key, self.params[key]))
