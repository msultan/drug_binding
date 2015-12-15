#!/bin/bash
#SBATCH --job-nam=clones
#SBATCH -o /home/msultan/research/kinase/drug_binding/2016/drug_binding/clone_log.out
#SBATCH --nodes=1
#SBATCH --gres=gpu:7
#SBATCH -t 23:59:00
#SBATCH -p longq

source ~/.bash_profile

for kinase in src abl syk
do
cd /home/msultan/research/kinase/drug_binding/2016/drug_binding/${kinase}_models/
python ../create_clones.py 
done
