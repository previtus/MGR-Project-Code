#!/bin/bash

# and finally the two 3gb

qsub -l walltime=47:30:00 expand_lr_minlen30_kfold.sh -l mem=64gb -l ncpus=8

qsub -l walltime=47:30:00 aggresive_expand_lr_minlen30_kfold.sh -l mem=64gb -l ncpus=8

