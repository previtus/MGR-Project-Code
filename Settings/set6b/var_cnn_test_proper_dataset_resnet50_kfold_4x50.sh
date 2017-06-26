#!/bin/bash

export PATH="/storage/brno2/home/previtus/anaconda2/bin:$PATH"
cd /auto/brno2/home/previtus/MGR-Project-Code/

python run_on_server.py Settings/set6b/var_cnn_test_proper_dataset_resnet50_kfold_4x50.py $PBS_JOBID
