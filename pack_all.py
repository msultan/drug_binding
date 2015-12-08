#!/bin/env python

import os
import subprocess
from multiprocessing import Pool
import glob
from msmbuilder.dataset import _keynat as keynat

packmol_script='''
tolerance 2.0

structure {input_path}
number 1
fixed 0. 0. 0. 0. 0. 0.
enterofmass
end structure
  
structure {imi_path}
number 1
inside sphere 0. 0. 0. 30.
end structure

add_amber_ter
output {output_path}
'''
wrk_dir = os.getcwd()

def add_drug((kinase,index,model)):
    print kinase,index,model
    input_path =os.path.join("./%s_unrefined_models/%s_%i.pdb"%(kinase,kinase,index))
    output_path = os.path.join("./%s_unrefined_drugged/%s_%i.pdb"%(kinase,kinase,index))
    imi_path = os.path.join("./imatinib/imatinib.pdb")
    script_path = os.path.join("./%s_%i.scrpt"%(kinase,index)) 
    with open(script_path,'w') as fout:
        fout.write(packmol_script.format(input_path=input_path,output_path=output_path,imi_path=imi_path))
    fout.close()
    cmd ="packmol < %s"%script_path
    os.system(cmd)
    os.remove(script_path)

for kinase in ["src","abl","syk"]:
    try:
        os.mkdir("%s_unrefined_drugged"%kinase)
    except:
        pass
    p=Pool(16)
    p.map(add_drug,[(kinase,index,model) for index,model in enumerate(sorted(glob.glob("./%s_unrefined_models/*.pdb"%kinase),key=keynat))])



