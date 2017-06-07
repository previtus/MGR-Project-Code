#!/bin/bash

qsub -l walltime=47:30:00 task_resnet152.sh -l mem=32gb -l ncpus=8