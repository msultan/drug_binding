#!/bin/bash
#SBATCH --job-nam=src
#SBATCH -o /home/msultan/research/kinase/drug_binding/2016/drug_binding/eq_src_log.out
#SBATCH --nodes=1
#SBATCH --gres=gpu:7
#SBATCH -t 23:59:00
#SBATCH -p longq

source ~/.bash_profile

cd /home/msultan/research/kinase/drug_binding/2016/drug_binding/src_models/

#run now
for i in {105..0..7} 
do
	for j in {0..6}
	do
		python ../simulate.py -k src -i $(($i + $j)) -c $(($i + $j))/src_wat_all.rst -p $(($i + $j))/src_wat.prmtop -d $j &
	done
	wait
done
