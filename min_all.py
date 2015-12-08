#!/bin/env/python
import os
import sys
import glob
from IPython import parallel
import shutil
import subprocess
from joblib import Parallel, delayed
import multiprocessing

def min_a_pdb(job_tuple):
    base_dir,kinase,pdb_id = job_tuple
    kinase_dir = os.path.join(base_dir,"%s_models"%kinase)
    os.chdir(kinase_dir)
    if os.path.isfile(os.path.join(kinase_dir,"%s/%s_wat_all.rst"%(pdb_id,kinase))) and os.stat("%s/%s_wat_all.rst"%(pdb_id,kinase)).st_size != 0:
          #already done
        return
    else:
        try:
            os.mkdir(os.path.join(kinase_dir,str(pdb_id)))
        except:
            pass
        job_dir = os.path.join(kinase_dir,str(pdb_id))
        os.chdir(job_dir)
        #copy the pdb file
        shutil.copy(os.path.join(base_dir,"%s_unrefined_drugged/%s_%s.pdb"%(kinase,kinase,pdb_id)),job_dir+"/prot.pdb")
        shutil.copy(os.path.join(base_dir,"tleap_%s.scrpt"%kinase),job_dir)

        subprocess.call(["tleap", "-f","tleap_%s.scrpt"%kinase])
          #now we min
        shutil.copy(os.path.join(base_dir,"min_1.in"), job_dir)
        shutil.copy(os.path.join(base_dir,"min_2.in"), job_dir)
        job1 = ["pmemd", "-O", "-i", "min_1.in", "-o", "%s_min_wat.out"%kinase, "-p" ,"%s_wat.prmtop"%kinase, "-c", "%s_wat.inpcrd"%kinase,"-r","%s_wat_min.rst"%kinase, "-ref", "%s_wat.inpcrd"%kinase]
        job2 = ["pmemd", "-O", "-i", "min_2.in", "-o", "%s_min_all.out"%kinase, "-p" ,"%s_wat.prmtop"%kinase, "-c", "%s_wat_min.rst"%kinase,"-r","%s_wat_all.rst"%kinase,]
        print(job1)
        print(job2)
        subprocess.call(job1)
        subprocess.call(job2)
        return





def main_function():

     client_list = parallel.Client(profile="default")
     client_list[:].execute("import os,subprocess,shutil")
     print("Running on:",len(client_list.ids))
     view = client_list.load_balanced_view()
     view.block = True
     kinase = sys.argv[1]
     print kinase
     base_dir = os.path.abspath(os.curdir)
     #num_cores = multiprocessing.cpu_count()
     flist = len(glob.glob("%s_unrefined_drugged/*.pdb"%kinase))
     print "Found %d files in %s_unrefined_drugged"%(flist,kinase)
     jobs = [(base_dir,kinase,run) for run in range(flist)]
     result = view.map_sync(min_a_pdb,jobs)



if __name__ == '__main__':
     main_function()
