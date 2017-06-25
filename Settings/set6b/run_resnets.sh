#!/bin/bash

# d1

qsub -l walltime=47:30:00 var_cnn_test_proper_dataset_resnet50_20.sh -l mem=32gb -l ncpus=8

qsub -l walltime=47:30:00 var_cnn_test_proper_dataset_resnet50_100.sh -l mem=32gb -l ncpus=8

