#!/bin/bash

# setting of the tasker

#qsub -l walltime=00:05:00 -q gpu -l nodes=1:ppn=1:gpu=1 -l mem=4gb  -N ${PWD##*/} task_v.sh

qsub -l walltime=40:00:00 task.sh -l mem=32gb -l ncpus=4
