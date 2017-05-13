from ExperimentRunner.ModelExperiments import run_many_models
import sys

settings_file = 'Settings/top_number_of_fc_blocks.py'
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


run_many_models(settings_file, job_id)
