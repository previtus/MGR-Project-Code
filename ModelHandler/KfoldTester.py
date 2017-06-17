import math
import numpy

def chunks(l, n):
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

def k_fold_crossvalidation(model, dataset, model_settings):
    k = model_settings["crossvalidation_k"]

    # idea is to generate k=4 folds of indices
    # with dataset having been shuffled already, we can just use the indices 0-number_of_images

    number_of_images_total = dataset.num_of_images
    number_of_images_total = 30

    print "Total of ", number_of_images_total, " images."

    indices = range(0, number_of_images_total)

    indices_in_fjords = chunks(indices, k)
    print indices_in_fjords
    print map(len,indices_in_fjords)

    # tests
    test = []
    for fjord in indices_in_fjords:
        test += fjord
    if not test == indices:
        print 'not the same!'

    selected = 2
    train_indices, validation_indices = kfold(indices_in_fjords, selected)
    print kfold(indices_in_fjords, 0)
    print kfold(indices_in_fjords, 1)

    [y1, y2] = dataset.getDataLabels_split_only_y(validation_split=model_settings["validation_split"])
    y = y1.tolist()+y2.tolist()
    y = range(100,160)
    print y

    selected_data = indices_to_data(validation_indices, y)
    print selected_data

    history = None
    return history