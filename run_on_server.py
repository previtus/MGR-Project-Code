from ExperimentRunner.ModelExperiments import experiment_runner
import sys

#settings_file = 'Settings/mix_model.py'
#settings_file = 'Settings/osm_only_model.py'
#settings_file = 'Settings/var_cnn_test.py'
#settings_file = 'Settings/models_versus_1200_299.py'
#settings_file = 'Settings/simple_hack.py'

#settings_file = 'Settings/shuffle_effective_1200.py'
#settings_file = 'Settings/finetune_tests_varAlong.py'

settings_file = 'Settings/debug_setting.py'

job_id = ''

if len(sys.argv) > 2:
    settings_file = (sys.argv[1])  # var1
    job_id = (sys.argv[2])  # var2

#main()
#main(set='1200x_markable_640x640', PIXELS=640)
#main(set='1200x_markable_299x299', PIXELS=299)
#main(set=name, PIXELS=pix)

# 5556x_mark_res_299x299 299
# 5556x_markable_640x640 640

print "job_id = ",job_id

experiment_runner(settings_file, job_id)
