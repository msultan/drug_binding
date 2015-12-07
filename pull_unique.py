#!/bin/env/python
'''
pull all the unique pdbs. Use pdbfixer to add hydrogen and save them again. 

'''
import os 
import mdtraj as mdt
import gzip
import pdbfixer
from multiprocessing import Pool

data_dir = os.path.join("/home/msultan/research/kinase/drug_binding/2016")
save_dir = os.getcwd()
def fix_model((kinase,index,model)):
     print kinase,model
     save_dir = os.path.join(os.getcwd(),"%s_refined_models"%kinase)
     fout = open((os.path.join(save_dir,"%d.pdb"%index),'wb'))
     fout.writelines(gzip.open(os.path.join(kinase_mdl_dir,"%s"%model,"model.pdb.gz")).read())     
     fout.close()
     #fixer = pdbfixer.PDBFixer(filename='temp%d.pdb'%index)
     #fixer.findMissingResidues()
     #fixer.findNonstandardResidues()
     #fixer.replaceNonstandardResidues()
     #fixer.findMissingAtoms()
     #fixer.addMissingAtoms()
     #fixer.addMissingHydrogens(7.0)
     #fixer.pdb.writeFile(fixer.topology, fixer.positions, open(os.path.join(save_dir,"%d.pdb"%index),'w'))
     #os.remove("temp%d.pdb"%index)
     return 

uni_name={}
uni_name["abl"] ="ABL1_HUMAN_D0"
uni_name["src"] = "SRC_HUMAN_D0"
uni_name["syk"] = "KSYK_HUMAN_D0"

for kinase in ["src","abl","syk"]:
    kinase_dir = os.path.join(data_dir,"%s_models"%kinase)
    kinase_mdl_dir = os.path.join(kinase_dir,"models","%s"%uni_name[kinase])
    models = [line.rstrip('\n') for line in open(os.path.join(kinase_mdl_dir,'unique-models.txt'))]
    try:
        os.mkdir("%s_unrefined_models"%kinase)
    except:
        pass 
    for index,model in enumerate(models):
        save_dir = os.path.join(os.getcwd(),"%s_unrefined_models"%kinase)
        fout = open(os.path.join(save_dir,"%s_%d.pdb"%(kinase,index)),'w')
        fout.writelines(gzip.open(os.path.join(kinase_mdl_dir,"%s"%model,"model.pdb.gz")).read())
        fout.close()
    print "Done with %s"%kinase
