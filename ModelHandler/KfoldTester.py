import math
import numpy
from Omnipresent import len_

def chunks(l, n):
    # Chunk data from list l into n fjords.
    a = numpy.array_split(numpy.array(l), n)
    b = []
    for i in a:
        b.append(i.tolist())
    return b

def kfold(indices_in_fjords, selected):
    # indices come like [] [] [] ... [], we want to select the one in <selected> as validation and rest as tests
    i = 0
    train_indices = []
    validation_indices = indices_in_fjords[selected]
    for fjord in indices_in_fjords:
        if i<>selected:
            train_indices += fjord
        i += 1
    return train_indices, validation_indices

def indices_to_data(any_indices, any_data):
    selected_data = [any_data[i] for i in any_indices]
    return selected_data

def select_data(indices, data):
    # select from data, while considering that data can be either list of items to directly select from
    # or it can be a list of size two, where we select from both items and later join
    selected = []
    i = len(data)
    if i == 2:
        first = data[0]
        second = data[1]

        first_selected = indices_to_data(indices, first)
        second_selected = indices_to_data(indices, second)

        selected = [numpy.array(first_selected), numpy.array(second_selected)]
    else:
        selected = indices_to_data(indices, data)

    return selected

def best_min(arr):
    # return the smallest value
    return min(arr)

def k_fold_crossvalidation(model, dataset, model_settings):
    # K fold crossvalidation scheme
    # includes proper loading of models, testing and processing of the results.
    from ModelHandler.ModelTester import load_features
    from ModelHandler.ModelTester import train_top_model

    k = model_settings["crossvalidation_k"]

    # idea is to generate k=4 folds of indices
    # with dataset having been shuffled already, we can just use the indices 0-number_of_images

    number_of_images_total = dataset.num_of_images

    print "Total of ", number_of_images_total, " images."

    indices = range(0, number_of_images_total)

    indices_in_fjords = chunks(indices, k)
    #print indices_in_fjords
    print "sizes of fjords:", map(len,indices_in_fjords)

    # (tests)
    test = []
    for fjord in indices_in_fjords:
        test += fjord
    if not test == indices:
        print 'not the same!'

    # fold indices are now prepared
    # collect all_inputs and all_outputs depending on the type of experiment we are running.
    all_inputs = []
    all_outputs = [] # outputs are always score labels
    all_outputs = dataset.getDataLabels_only_y()

    features = []
    active_model = None
    if model_settings["model_type"] is 'img_osm_mix' or model_settings["model_type"] is 'simple_cnn_with_top':
        filename_features_train = model_settings["filename_features_train"]
        filename_features_test = model_settings["filename_features_test"]
        [train_data, _, validation_data, _] = load_features(filename_features_train, filename_features_test, None, None)

        features = numpy.append(train_data, validation_data, 0)

    #arr_test = arr[0:split_at]
    #arr_val = arr[split_at:]


    # TODO: MODEL_TYPE_SPLIT
    if model_settings["model_type"] is 'simple_cnn_with_top':
        print "Prepare all_inputs and all_outputs for Image only model."
        # inputs are all the images, but for our model its the features
        all_inputs = features
        active_model = model[1]

    elif model_settings["model_type"] is 'osm_only':
        print "Prepare all_inputs and all_outputs for OSM only model."
        # inputs are all the osm vectors
        all_inputs = dataset.getDataLabels_only_osm()
        active_model = model[0]

    elif model_settings["model_type"] is 'img_osm_mix':
        print "Prepare all_inputs and all_outputs for Mixed model."
        # inputs list of features and osm vectors
        osms = dataset.getDataLabels_only_osm()
        all_inputs = [osms, features]
        active_model = model[1]

        print len_(osms), "and", len_(features)
    else:
        print "Yet to be programmed."

    # save active_models weights, so we don't cheat by cumulating better and better results...
    initial_weights = active_model.get_weights()

    print "Sizes of all_inputs:", len_(all_inputs), "and all_outputs:", len_(all_outputs)

    # variables for remembering data from histories
    last_training_errors = []
    best_training_errors = []
    last_validation_errors = []
    best_validation_errors = []
    all_histories_of_this_model = []

    last_training_measure = []
    best_training_measure = []
    last_validation_measure = []
    best_validation_measure = []

    for selected_fjord in range(0,k):
        active_model.set_weights(initial_weights)

        train_indices, valid_indices = kfold(indices_in_fjords, selected_fjord)

        train_inputs = select_data(train_indices, all_inputs)
        valid_inputs = select_data(valid_indices, all_inputs)
        train_outputs = select_data(train_indices, all_outputs)
        valid_outputs = select_data(valid_indices, all_outputs)

        print "selected_fjord", selected_fjord
        print "Sizes of train_inputs:", len_(train_inputs), "and train_outputs:", len_(train_outputs)
        print "Sizes of valid_inputs:", len_(valid_inputs), "and valid_outputs:", len_(valid_outputs)

        # into training and result collecting
        history = train_top_model(active_model, model_settings, train_inputs, train_outputs, valid_inputs, valid_outputs)
        #print history

        measure = 'mean_absolute_error'
        error = 'loss'
        val_measure = 'val_' + measure
        val_error = 'val_' + error
        '''
         {'val_mean_absolute_error':
             [0.00036219754838384688, 7.0134797169885132e-06, 3.973643103449831e-08, 3.973643103449831e-08, 3.973643103449831e-08],
         'loss':
             [0.34813621640205383, 0.16262358427047729, 0.19959338009357452, 0.16045540571212769, 0.16040021181106567],
         'mean_absolute_error':
             [0.50139808654785156, 0.22280247509479523, 0.25902602076530457, 0.21229584515094757, 0.21108284592628479],
         'val_loss':
             [1.7484823899849289e-07, 9.398822692352482e-11, 4.7369517129061591e-15, 4.7369517129061591e-15, 4.7369517129061591e-15]
         }
        '''

        # process history!
        all_histories_of_this_model.append(history)
        last_training_errors.append( history[error][-1] )
        last_validation_errors.append( history[val_error][-1] )

        last_training_measure.append( history[measure][-1] )
        last_validation_measure.append( history[val_measure][-1] )

        best_training_errors.append( best_min(history[error]) )
        best_validation_errors.append( best_min(history[val_error]) )

        best_training_measure.append( best_min(history[measure]) )
        best_validation_measure.append( best_min(history[val_measure]) )

    print "error", error
    print "last_training_errors", last_training_errors
    print "best_training_errors", best_training_errors
    print "last_validation_errors", last_validation_errors
    print "best_validation_errors", best_validation_errors

    print "measure", measure
    print "last_training_measure", last_training_measure
    print "best_training_measure", best_training_measure
    print "last_validation_measure", last_validation_measure
    print "best_validation_measure", best_validation_measure

    print "all_histories_of_this_model", all_histories_of_this_model

    special_history_dictionary = {}
    special_history_dictionary["last_training_errors"] = last_training_errors
    special_history_dictionary["best_training_errors"] = best_training_errors
    special_history_dictionary["last_validation_errors"] = last_validation_errors
    special_history_dictionary["best_validation_errors"] = best_validation_errors

    special_history_dictionary["last_training_measure"] = last_training_measure
    special_history_dictionary["best_training_measure"] = best_training_measure
    special_history_dictionary["last_validation_measure"] = last_validation_measure
    special_history_dictionary["best_validation_measure"] = best_validation_measure

    special_history_dictionary["all_histories_of_this_model"] = all_histories_of_this_model

    history = special_history_dictionary
    return history
