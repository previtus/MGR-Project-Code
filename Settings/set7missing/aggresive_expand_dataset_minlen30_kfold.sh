#!/bin/bash

export PATH="/storage/brno2/home/previtus/anaconda2/bin:$PATH"
cd /auto/brno2/home/previtus/MGR-Project-Code/

python run_on_server.py Settings/set7missing/aggresive_expand_dataset_minlen30_kfold.py $PBS_JOBID
