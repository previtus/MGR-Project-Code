#!/bin/bash

qsub -l walltime=23:30:00 img.sh -l mem=32gb -l ncpus=8
