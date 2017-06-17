
def k_fold_crossvalidation(model, dataset, model_settings):
    k = model_settings["crossvalidation_k"]

    # idea is to generate k=4 folds of indices
    # with dataset having been shuffled already, we can just use the indices 0-number_of_images

    number_of_images_total = dataset.num_of_images

    number_of_images_total = 97

    print "Total of ", number_of_images_total, " images."

    indices = range(0, number_of_images_total)

    last_index = 0
    # indices in k folds
    for i in range(0,k):
        print "doing", i, "outta", k

        #floor
        to_index = int( (i+1) * round(float(number_of_images_total) / float(k)) )

        if (i+1)==k:
            to_index = number_of_images_total

        print "from", last_index, "to", to_index
        last_index = to_index+1

    history = None
    return history