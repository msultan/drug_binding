#!/bin/bash
#SBATCH --job-nam=syk
#SBATCH -o /home/msultan/research/kinase/drug_binding/2016/drug_binding/syk.out
#SBATCH -p longq
#SBATCH -N 1
#SBATCH -t 23:59:00

module load openmpi/gcc/64/1.8.5
echo $CUDA_VISIBLE_DEVICES
ipcluster start &
cd /home/msultan/research/kinase/drug_binding/2016/drug_binding/
python min_all.py syk

wait 

