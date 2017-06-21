#!/bin/bash

qsub -l walltime=23:30:00 set5_w32_depth1_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w32_depth2_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w32_depth3_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w32_depth4_d1.sh -l mem=32gb -l ncpus=8

qsub -l walltime=23:30:00 set5_w64_depth1_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w64_depth2_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w64_depth3_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w64_depth4_d1.sh -l mem=32gb -l ncpus=8

qsub -l walltime=23:30:00 set5_w128_depth1_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w128_depth2_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w128_depth3_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w128_depth4_d1.sh -l mem=32gb -l ncpus=8

qsub -l walltime=23:30:00 set5_w256_depth1_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w256_depth2_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w256_depth3_d1.sh -l mem=32gb -l ncpus=8
qsub -l walltime=23:30:00 set5_w256_depth4_d1.sh -l mem=32gb -l ncpus=8

