from ModelHandler.CreateModel.ModelsFunctions import load_features, build_top_model, train_top_model, save_model_history
from Downloader.ImageHelpers import len_

def TestTopModel(dataset, model_name, filename_features_train, filename_features_test, filename_history, img_name):
    [x, y, x_val, y_val] = dataset.getDataLabels_split(validation_split=0.25)
    #[test_generator, val_generator, number_in_test, number_in_val] = dataset.getGenerators(validation_split=0.25)

    [train_data, train_labels, validation_data, validation_labels] = load_features(filename_features_train, filename_features_test, y, y_val)

    print "input shape of features", len_(train_data), "and labels", len_(train_labels)
    # Report feature output sizes

    # Try top models - regular with fixed size or the "heatmap"
    model = build_top_model(train_data.shape[1:], 3)

    epochs = 20 #150
    save_img_name = model_name
    history = train_top_model(model, train_data, train_labels, epochs, validation_data, validation_labels, save_img_name=None)

    save_model_history(history, filename_history, img_name)

    return history
