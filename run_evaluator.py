from Evaluator.Evaluator import evaluator
import sys

from DatasetHandler.FileHelperFunc import get_project_folder
ABS_PATH_TO_PRJ = get_project_folder()

folder_path = ABS_PATH_TO_PRJ + 'Data/ModelFiles/'
#folder_path = '/home/ekmek/Vitek/Mgr project/MGR-Project-Code/Data/ModelFiles/'
#folder_path = '/home/ekmek/Vitek/MGR-Project-Code/Data/ModelFiles/'
# IMG
IMG_model_file = folder_path + 'SelectedModels/1769353.arien-pro.ics.muni.cz_TypesOfModels_monoTest_IMG_kfold_d3/models/imagemodel_resnet50.h5_top.h5'
IMG_settings_file = 'Settings/set3/type_of_model_img_kfold_d3.py'

# MIX
MIX_model_file = folder_path + 'SelectedModels/1761335.arien-pro.ics.muni.cz_TypesOfModels_monoTest_MIX_kfold_d3/models/mixmodel_resnet50.h5_top.h5'
MIX_settings_file = 'Settings/set3/type_of_model_mix_kfold_d3.py'

# OSM
OSM_model_file = folder_path + 'SelectedModels/1761336.arien-pro.ics.muni.cz_TypesOfModels_monoTest_OSM_kfold_d3/models/osmmodel_resnet50.h5_osmtop.h5'
OSM_settings_file = 'Settings/set3/type_of_model_osm_kfold_d3.py'


# OSM Flagship Model !
OSM_model_file = folder_path + 'SelectedModels/1771032.arien-pro.ics.muni.cz_set5_w64_depth2_d1/models/osm_resnet50.h5_osmtop.h5'
OSM_settings_file = 'Settings/set5/set5_w64_depth2_d1.py'


if len(sys.argv) > 2:
    model_file = (sys.argv[1])  # var1
    settings_file = (sys.argv[2])  # var2

img_mse, img_mae = evaluator(IMG_model_file, IMG_settings_file, 'marked_from_img_1769353.geojson')
mix_mse, mix_mae = evaluator(MIX_model_file, MIX_settings_file, 'marked_from_mix_1761335.geojson')
#osm_mse, osm_mae = evaluator(OSM_model_file, OSM_settings_file)

'''
print "-------------------------------------"
print "IMG mse =", img_mse, "; mae = ", img_mae
print "MIX mse =", mix_mse, "; mae = ", mix_mae
print "OSM mse =", osm_mse, "; mae = ", osm_mae
'''

#from Evaluator.Evaluator import test_marking
#geojsonpath = '/home/ekmek/Vitek/____out_marked-json-files/marked_from_osm-set3type_of_model_osm_kfold_d3.geojson'
#test_marking(geojsonpath)
