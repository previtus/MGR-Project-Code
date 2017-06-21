#!/bin/bash

# d1

qsub -l walltime=47:30:00 set4b_pixelSize_img_299_d7.sh -l mem=32gb -l ncpus=8

qsub -l walltime=47:30:00 set4b_pixelSize_mix_299_d7.sh -l mem=32gb -l ncpus=8

