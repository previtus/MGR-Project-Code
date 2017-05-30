#!/bin/bash

# qsub -l walltime=23:30:00 mix299.sh -l mem=32gb -l ncpus=8

qsub -l walltime=23:30:00 mix.sh -l mem=32gb -l ncpus=8

# qsub -l walltime=23:30:00 models_30m_640px.sh -l mem=32gb -l ncpus=8

qsub -l walltime=23:30:00 models_10m_640px.sh -l mem=32gb -l ncpus=8

qsub -l walltime=23:30:00 osm.sh -l mem=32gb -l ncpus=8

# qsub -l walltime=23:30:00 img299.sh -l mem=32gb -l ncpus=8

qsub -l walltime=23:30:00 img.sh -l mem=32gb -l ncpus=8
