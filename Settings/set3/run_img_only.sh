#!/bin/bash

# img only

qsub -l walltime=47:30:00 type_of_model_img_kfold_d1.sh -l mem=32gb -l ncpus=8

qsub -l walltime=47:30:00 type_of_model_img_kfold_d2.sh -l mem=32gb -l ncpus=8

qsub -l walltime=47:30:00 type_of_model_img_kfold_d3.sh -l mem=32gb -l ncpus=8

qsub -l walltime=47:30:00 type_of_model_img_kfold_d4.sh -l mem=32gb -l ncpus=8
