from Evaluator.Evaluator import evaluator
import sys

from DatasetHandler.FileHelperFunc import get_project_folder
ABS_PATH_TO_PRJ = get_project_folder()

folder_path = ABS_PATH_TO_PRJ + 'Data/ModelFiles/'

# IMG
IMG_model_file = folder_path + 'SelectedModels/1769353.arien-pro.ics.muni.cz_TypesOfModels_monoTest_IMG_kfold_d3/models/imagemodel_resnet50.h5_top.h5'
IMG_settings_file = 'Settings/set3_crossval-one-model-on-one-dataset/type_of_model_img_kfold_d3.py'

# OSM Flagship Model !
OSM_model_file = folder_path + 'SelectedModels/1771032.arien-pro.ics.muni.cz_set5_w64_depth2_d1/models/osm_resnet50.h5_osmtop.h5'
OSM_settings_file = 'Settings/set5-osm-model-variable-widths-depths/set5_w64_depth2_d1.py'

# MIX Flagship Model !
MIX_model_file = folder_path + 'SelectedModels/1788956.arien-pro.ics.muni.cz_builds_aggresive_expand_dataset_normalmarkable_kfold/models/expanded: 5556x_markable_640x640_2x_agressive_expanded_resnet50.h5_top.h5'
MIX_settings_file = 'Settings/set7_dataset-aggressive-expansion/builds_aggresive_expand_dataset_normalmarkable_kfold.py'

if len(sys.argv) > 2:
    model_file = (sys.argv[1])  # var1
    settings_file = (sys.argv[2])  # var2

#img_mse, img_mae = evaluator(IMG_model_file, IMG_settings_file, 'marked_from_img_1769353.geojson')
#mix_mse, mix_mae = evaluator(MIX_model_file, MIX_settings_file, 'marked_from_mix_flag1788956.geojson', )

custom_target_geojson = None
osm_mse, osm_mae = evaluator(OSM_model_file, OSM_settings_file, 'NVMpraha_part_osm_marked.geojson', custom_target_geojson,
                             show_segments_histo_stats=True, actually_save=False)

'''
geojson_to_be_marked = 'EXAMPLE_GEOJSON.json'
segments_for_the_geojson = 'EXAMPLE_SEGMENTS.dump'
custom_target_geojson = [geojson_to_be_marked, segments_for_the_geojson]
'''