#!/bin/env python
import numpy as np
import mdtraj as mdt
import glob,os
from test_packing import base_dir
from test_sequence import match_seq
'''
Test to make sure we send the right stuff to fah
'''
N=5
dir_suffix = "_models/"

def test_min():
    for kinase in ["src","abl","syk"]:
        mdl_dir = os.path.join(base_dir,kinase+dir_suffix)
        pdb_list = glob.glob("%s/RUN*/*.pdb"%(mdl_dir))
        to_test_list  = np.random.choice(pdb_list,N,replace=False)
        for pdb_file in to_test_list:
            print "Testing %s pdb %s"%(kinase,pdb_file)
            t = mdt.load(pdb_file)
            #check that seq matches up
            curr_seq = ''.join([i.code for i in t.top.residues if i.is_protein])
            assert(match_seq(kinase,curr_seq))
