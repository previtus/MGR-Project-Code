#!/bin/bash


qsub -l walltime=47:30:00 builds_aggresive_expand_dataset_normalmarkable_kfold.sh -l mem=64gb -l ncpus=8

