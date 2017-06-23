#!/bin/bash


qsub -l walltime=47:30:00 aggresive_expand_dataset_minlen30_kfold.sh -l mem=64gb -l ncpus=8

