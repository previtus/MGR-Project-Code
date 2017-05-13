#!/bin/bash

export PATH="/storage/brno2/home/previtus/anaconda2/bin:$PATH"
cd /auto/brno2/home/previtus/MGR-Project-Code/

#                 dataset epochs name
#python run_example.py
#python run_example.py 4000 250 -4kSubset
#python run_example.py > ../Logs/log_${PBS_JOBID}.txt
#python run_example.py > ../Logs/log.txt

python run_on_server.py Settings/top_number_of_fc_blocks.py $PBS_JOBID

