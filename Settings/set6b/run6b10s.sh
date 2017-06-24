#!/bin/bash

# d1


qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_vgg16_100.sh -l mem=64gb -l ncpus=8

qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_vgg19_100.sh -l mem=128gb -l ncpus=8

qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_inception_v3_100.sh -l mem=128gb -l ncpus=8

qsub -l walltime=167:30:00 var_cnn_test_proper_dataset_xception_100.sh -l mem=128gb -l ncpus=8
