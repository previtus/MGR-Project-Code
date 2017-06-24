#!/bin/bash

# d1

qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_inception_v3.sh -l mem=128gb -l ncpus=8

qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_xception.sh -l mem=128gb -l ncpus=8

