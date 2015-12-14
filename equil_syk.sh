#!/bin/bash
#SBATCH --job-nam=syk
#SBATCH -o /home/msultan/research/kinase/drug_binding/2016/drug_binding/eq_syk_log.out
#SBATCH --nodes=1
#SBATCH --gres=gpu:7
#SBATCH -t 23:59:00
#SBATCH -p longq

source ~/.bash_profile

cd /home/msultan/research/kinase/drug_binding/2016/drug_binding/syk_models/

#run now
for i in {0..105..7} 
do
	for j in {0..6}
	do
		python ../simulate.py -k syk -i $(($i + $j)) -c $(($i + $j))/syk_wat_all.rst -p $(($i + $j))/syk_wat.prmtop -d $j &
	done
	wait
done
