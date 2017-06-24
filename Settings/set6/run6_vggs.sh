#!/bin/bash

# d1

qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_vgg16.sh -l mem=64gb -l ncpus=8

qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_vgg19.sh -l mem=128gb -l ncpus=8

