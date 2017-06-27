#!/bin/bash

qsub -l walltime=23:30:00 var_cnn_test_proper_dataset_299.sh -l mem=128gb -l ncpus=8
