#!/bin/env/python
'''
Added some tests to make sure we have a drug in "N" randomly chosen pdbs
'''
import glob
import numpy as np
import os
import mdtraj as mdt
N = 10 
base_dir = os.path.join("/home/msultan/research/kinase/drug_binding/2016/drug_binding")
drug_dir_suffix="_unrefined_drugged"


def test_packing():
    for kinase in ["src","abl","syk"]:
        drug_dir = os.path.join(base_dir,kinase+drug_dir_suffix)
        pdb_list = glob.glob("%s/*.pdb"%drug_dir)
        to_test_list  = np.random.choice(pdb_list,N,replace=False)
        for pdb_file in to_test_list:
            t = mdt.load(pdb_file)
            #check that LIG exists
            assert(np.any([i.name=='LIG' for i in t.top.residues]))
            assert(np.count_nonzero([i for i in t.top.atoms if i.residue.name=='LIG'])==69)
        print "Drug found in %d pdbs for %s with 69 atoms in each case"%(N,kinase)
