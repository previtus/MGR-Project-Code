#!/bin/bash

qsub -l walltime=23:30:00 task_resnet152_640.sh -l mem=32gb -l ncpus=8