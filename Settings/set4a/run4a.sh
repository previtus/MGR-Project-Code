#!/bin/bash

# d1

qsub -l walltime=47:30:00 set4a_MinEdgeSize_mix_len10_kfold_d5.sh -l mem=32gb -l ncpus=8

qsub -l walltime=47:30:00 set4a_MinEdgeSize_mix_len20_kfold_d5.sh -l mem=32gb -l ncpus=8


qsub -l walltime=47:30:00 set4a_MinEdgeSize_img_len10_kfold_d5.sh -l mem=32gb -l ncpus=8

qsub -l walltime=47:30:00 set4a_MinEdgeSize_img_len20_kfold_d5.sh -l mem=32gb -l ncpus=8
