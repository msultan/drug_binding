#!/bin/env python

'''
Script to make sure ensembler modeled in the right sequence 
'''

import glob
import numpy as np
import os
import mdtraj as mdt 
N = 10  
base_dir = os.path.join("/home/msultan/research/kinase/drug_binding/2016/drug_binding")
drug_dir_suffix="_unrefined_models"

actual_seq={}
actual_seq['src'] = "LRLEVKLGQGCFGEVWMGTWNGTTRVAIKTLKPGTMSPEAFLQEAQVMKKLRHEKLVQLYAVVSEEPIYIVTEYMSKGSLLDFLKGETGKYLRLPQLVDMAAQIASGMAYVERMNYVHRDLRAANILVGENLVCKVADFGLARLIEDNEYTARQGAKFPIKWTAPEAALYGRFTIKSDVWSFGILLTELTTKGRVPYPGMVNREVLDQVERGYRMPCPPECPESLHDLMCQCWRKEPEERPTFEYLQAFLEDYF"

actual_seq["abl"] = "ITMKHKLGGGQYGEVYEGVWKKYSLTVAVKTLKEDTMEVEEFLKEAAVMKEIKHPNLVQLLGVCTREPPFYIITEFMTYGNLLDYLRECNRQEVNAVVLLYMATQISSAMEYLEKKNFIHRDLAARNCLVGENHLVKVADFGLSRLMTGDTYTAHAGAKFPIKWTAPESLAYNKFSIKSDVWAFGVLLWEIATYGMSPYPGIDLSQVYELLEKDYRMERPEGCPEKVYELMRACWQWNPSDRPSFAEIHQAF"

actual_seq["syk"] = "TLEDKELGSGNFGTVKKGYYQMKKVVKTVAVKILKNEANDPALKDELLAEANVMQQLDNPYIVRMIGICEAESWMLVMEMAELGPLNKYLQQNRHVKDKNIIELVHQVSMGMKYLEESNFVHRDLAARNVLLVTQHYAKISDFGLSKALRADENYYKAQTHGKWPVKWYAPECINYYKFSSKSDVWSFGVLMWEAFSYGQKPYRGMKGSEVTAMLEKGERMGCPAGCPREMYDLMNLCWTYDVENRPGFAAVELRLRNYYY"

def match_seq(kinase,sequence):
    return (sequence==actual_seq[kinase])



def test_ensembler():
    for kinase in ["src","abl","syk"]:
        drug_dir = os.path.join(base_dir,kinase+drug_dir_suffix)
        pdb_list = glob.glob("%s/*.pdb"%drug_dir)
        to_test_list  = np.random.choice(pdb_list,N,replace=False)
        for pdb_file in to_test_list:
            t = mdt.load(pdb_file)
            #check that seq matches up
            curr_seq = ''.join([i.code for i in t.top.residues if i.is_protein])
            assert(match_seq(kinase,curr_seq))
        print "%s sequence successfully matched in %d pdbs"%(kinase,N)
