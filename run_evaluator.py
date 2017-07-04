from Evaluator.Evaluator import evaluator
import sys

#folder_path = '/home/ekmek/Vitek/Mgr project/MGR-Project-Code/Data/ModelFiles/'
folder_path = '/home/ekmek/Vitek/MGR-Project-Code/Data/ModelFiles/'
# IMG
IMG_model_file = folder_path + 'SelectedModels/1769353.arien-pro.ics.muni.cz_TypesOfModels_monoTest_IMG_kfold_d3/models/imagemodel_resnet50.h5_top.h5'
IMG_settings_file = 'Settings/set3/type_of_model_img_kfold_d3.py'

# MIX
MIX_model_file = folder_path + 'SelectedModels/1761335.arien-pro.ics.muni.cz_TypesOfModels_monoTest_MIX_kfold_d3/models/mixmodel_resnet50.h5_top.h5'
MIX_settings_file = 'Settings/set3/type_of_model_mix_kfold_d3.py'

# OSM
OSM_model_file = folder_path + 'SelectedModels/1761336.arien-pro.ics.muni.cz_TypesOfModels_monoTest_OSM_kfold_d3/models/osmmodel_resnet50.h5_osmtop.h5'
OSM_settings_file = 'Settings/set3/type_of_model_osm_kfold_d3.py'

if len(sys.argv) > 2:
    model_file = (sys.argv[1])  # var1
    settings_file = (sys.argv[2])  # var2

#evaluator(IMG_model_file, IMG_settings_file)
#evaluator(MIX_model_file, MIX_settings_file)
evaluator(OSM_model_file, OSM_settings_file)
