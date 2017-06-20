#!/bin/bash

export PATH="/storage/brno2/home/previtus/anaconda2/bin:$PATH"
cd /auto/brno2/home/previtus/MGR-Project-Code/

python run_on_server.py Settings/set3/type_of_model_osm_kfold_d4.py $PBS_JOBID
