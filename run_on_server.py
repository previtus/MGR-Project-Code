from ExperimentRunner.ModelExperiments import experiment_runner
import sys

settings_file = 'Settings/minimal_model.py'
job_id = ''

# python run_on_server.py SETTINGS_PATH UNIQUE_EXPERIMENT_ID
if len(sys.argv) > 2:
    settings_file = (sys.argv[1])  # var1
    job_id = (sys.argv[2])  # var2

print "job_id = ",job_id

experiment_runner(settings_file, job_id)
