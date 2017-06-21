#!/bin/bash

export PATH="/storage/brno2/home/previtus/anaconda2/bin:$PATH"
cd /auto/brno2/home/previtus/MGR-Project-Code/

python run_on_server.py Settings/set4a/set4a_MinEdgeSize_img_len10_kfold_d5.py $PBS_JOBID
