#!/bin/bash

qsub -l walltime=47:30:00 var_cnn_test_proper_dataset_inception_v3_kfold299.sh -l mem=128gb -l ncpus=8

qsub -l walltime=47:30:00 var_cnn_test_proper_dataset_xception_kfold299.sh -l mem=128gb -l ncpus=8

qsub -l walltime=47:30:00 var_cnn_test_proper_dataset_vgg19_kfold299.sh -l mem=64gb -l ncpus=8

qsub -l walltime=47:30:00 var_cnn_test_proper_dataset_vgg16_kfold299.sh -l mem=64gb -l ncpus=8

qsub -l walltime=47:30:00 var_cnn_test_proper_dataset_resnet50_kfold299.sh -l mem=64gb -l ncpus=8
