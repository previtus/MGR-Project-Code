from Evaluator.Evaluator import evaluator
import sys

model_file = '/home/ekmek/Vitek/Mgr project/MGR-Project-Code/Data/ModelFiles/SelectedModels/1769353.arien-pro.ics.muni.cz_TypesOfModels_monoTest_IMG_kfold_d3/models/imagemodel_resnet50.h5_top.h5'
settings_file = 'Settings/set3/type_of_model_img_kfold_d3.py'

if len(sys.argv) > 2:
    model_file = (sys.argv[1])  # var1
    settings_file = (sys.argv[2])  # var2

evaluator(model_file, settings_file)