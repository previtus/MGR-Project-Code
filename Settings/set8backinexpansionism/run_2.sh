#!/bin/bash

# then second 6gb

qsub -l walltime=47:30:00 aggresive_expand_lr_markable_kfold.sh -l mem=64gb -l ncpus=8

