Contains selected experiment run results, alongside with their histories (in /history/*.npy file), graphs and the models themselves (in models/*.h5).

For using these models for new dataset evaluation we need both the h5 file and the Setting file which was used with the experiment.
Call evaluator from Evaluator/Evalutator.py with following example syntax:

MIX_model_file = folder_path + '/models/expanded: 5556x_markable_640x640_2x_agressive_expanded_resnet50.h5_top.h5'
MIX_settings_file = folder_path + '/builds_aggresive_expand_dataset_normalmarkable_kfold.py'

evaluator(MIX_model_file, MIX_settings_file, 'marked_from_mix_flag1788956.geojson')