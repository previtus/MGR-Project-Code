#!/bin/bash

export PATH="/storage/brno2/home/previtus/anaconda2/bin:$PATH"
cd /auto/brno2/home/previtus/MGR-Project-Code/

python run_on_server.py Settings/set6c_299/var_cnn_test_proper_dataset_xception_kfold299.py $PBS_JOBID
