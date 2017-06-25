#!/bin/bash

# lets say we can start with one 6gb

qsub -l walltime=47:30:00 expand_lr_markable_kfold.sh -l mem=64gb -l ncpus=8

