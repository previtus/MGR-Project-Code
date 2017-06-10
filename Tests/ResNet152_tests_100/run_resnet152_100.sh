#!/bin/bash

qsub -l walltime=167:30:00 task_resnet152_100.sh -l mem=32gb -l ncpus=8