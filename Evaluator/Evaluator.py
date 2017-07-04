import ExperimentRunner.SettingsDefaults as SettingsDefaults

import ModelHandler.ModelOI as ModelOI
import ModelHandler.ModelGenerator as ModelGenerator
import ModelHandler.ModelTester as ModelTester
import DatasetHandler as DatasetHandler
from Omnipresent import len_

def evaluator_load_model(model_file, settings_file, verbose=False):
    ### LOAD skeleton of model and dataset
    Settings = SettingsDefaults.load_settings_from_file(settings_file, '', verbose=False)
    if verbose:
        print Settings

    Settings["models"][0]["test_existence_of_images"] = False
    Settings["models"][0]["evaluation_after_training"] = True
    Settings["models"][0]["model_shape_filename"] = "tmp.png"
    model_settings = Settings["models"][0]

    models = ModelGenerator.get_cnn_models(Settings)
    models = ModelGenerator.get_top_models(models, None, Settings)

    if Settings["interrupt"]:
        return 365
    if Settings["report_on_models"]:
        ModelGenerator.report_models(models, Settings)

    if verbose:
        ModelOI.save_visualizations(models, Settings)

    ### WEIGHTS to model from file
    if verbose:
        print len(models), model_file

    loaded_model = models[0]
    if model_settings["model_type"] is 'osm_only':
        # osm model doesn't have a base
        loaded_model[0].load_weights(model_file)
        model_base = None
        model_top = loaded_model[0]
    else:
        loaded_model[1].load_weights(model_file)
        model_base = loaded_model[0]
        model_top = loaded_model[1]

    if verbose:
        #print "BASE MODEL"
        #model_base.summary()

        print "TOP MODEL"
        model_top.summary()

    return model_base, model_top, model_settings

def evaluator_test_on_dataset(model_base, model_top, model_settings, x, osm):
    if model_settings["model_type"] is 'simple_cnn_with_top':
        labels_base = model_base.predict(x, batch_size=32, verbose=1)
        labels_predicted = model_top.predict(labels_base, batch_size=32, verbose=1)
    elif model_settings["model_type"] is 'img_osm_mix':
        labels_base = model_base.predict(x, batch_size=32, verbose=1)
        osm_input = osm
        labels_predicted = model_top.predict([osm_input, labels_base], batch_size=32, verbose=1)
    elif model_settings["model_type"] is 'osm_only':
        osm_input = osm
        labels_predicted = model_top.predict(osm_input, batch_size=32, verbose=1)

    print len_(labels_predicted)
    labels_return = []
    for label in labels_predicted:
        labels_return.append(label[0])
    return labels_return

## ---------- debug test functions
def load_tmp_dataset():
    model_settings = {}
    # HACK
    model_settings["dataset_name"] = "miniset_640px"
    model_settings["pixels"] = 640
    model_settings["number_of_images"] = None
    model_settings["seed"] = 13

    #Settings["models"][0]["dump_file_override"] = 'SegmentsData.dump'
    model_settings["dump_file_override"] = 'SegmentsData_mark100.dump'

    dataset = DatasetHandler.CreateDataset.load_custom(model_settings["dataset_name"], model_settings["pixels"],
                                                       desired_number=model_settings["number_of_images"],
                                                       seed=model_settings["seed"],
                                                       filename_override=model_settings["dump_file_override"])
    [x, y] = dataset.getDataLabels()
    osm = dataset.getDataLabels_only_osm()
    print len_(x), len_(y), len_(osm)
    return x, y, osm

def evaluator_on_tmp(model_file, settings_file):
    model_base, model_top, model_settings = evaluator_load_model(model_file, settings_file)
    x, y_ref, osm = load_tmp_dataset()
    y_pred = evaluator_test_on_dataset(model_base, model_top, model_settings, x, osm)
    print y_ref, y_pred
    from sklearn.metrics import mean_squared_error, mean_absolute_error
    mae = mean_absolute_error(y_ref, y_pred)
    mse = mean_squared_error(y_ref, y_pred)
    return mse, mae
## ENDOF---------- debug test functions


def test_marking(geo_json_path):
    path_to_segments_file = default_segments_path()
    lists, Segments = loadDataFromSegments(path_to_segments_file, None)
    GeoJSON = loadGeoJson(geo_json_path)

    from Functions import traverseGeoJSON
    traverseGeoJSON(GeoJSON, Segments)


from Functions import *
def evaluator(model_file, settings_file):
    model_base, model_top, model_settings = evaluator_load_model(model_file, settings_file)

    # Load data!
    path_to_segments_file = default_segments_path()
    lists, Segments = loadDataFromSegments(path_to_segments_file, None)
    #lists = small_lists(lists)

    print "BEFORE MARKING"
    analyze_lists(lists)

    y_ref = lists[1]
    osm = osm_from_lists(lists)
    x = None
    segment_ids = lists[3]

    #print "i have", len_(osm)
    #x, y_ref, osm = load_tmp_dataset()
    #print "this works though", len_(osm)

    y_pred = evaluator_test_on_dataset(model_base, model_top, model_settings, x, osm)

    pred_list = [lists[0], y_pred, lists[2], lists[3]]
    print "AFTER MARKING"
    analyze_lists(pred_list)

    EvaluatedData = prepEvaluatedData(y_pred, segment_ids)
    Altered = AlterSegments(EvaluatedData, Segments, only_unknown_scores=True)

    GeoJSON = loadDefaultGEOJSON()
    evaluated_geojson = markGeoJSON(GeoJSON, Altered)
    path_geojson_out = 'marked_from_osm-set3type_of_model_osm_kfold_d3.geojson'
    saveGeoJson(evaluated_geojson, path_geojson_out)

    # Ex post testing
    DefaultSegments = DataOperations.LoadDataFile(path_to_segments_file)
    traverseGeoJSON(evaluated_geojson, DefaultSegments)


    #print y_ref, y_pred

    from sklearn.metrics import mean_squared_error, mean_absolute_error
    mae = mean_absolute_error(y_ref, y_pred)
    mse = mean_squared_error(y_ref, y_pred)

    np.savetxt('y_ref.out', y_ref, delimiter=',')
    np.savetxt('y_pred.out', y_pred, delimiter=',')

    return mse, mae

