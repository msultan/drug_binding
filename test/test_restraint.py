#!/bin/env python

'''
Make sure we state/system/integrator xmls have the necessary extra restraint
'''
import numpy as np
import mdtraj as mdt
import simtk.openmm as mm
from test_sequence import *

def test_restraints():
    for kinase in ["src","abl","syk"]:
        wrk_dir = os.path.join(base_dir,kinase)
        run_list = glob.glob("%s/RUN*"%wrk_dir)
        to_test_list  = np.random.choice(run_list,N,replace=False)
        for run_dir in to_test_list:
            state = mm.XmlSerializer.deserialize("%s/state0.xml"%run_dir)
            system = mm.XmlSerializer.deserialize("%s/system.xml"%run_dir)
            integrator = mm.XmlSerializer.deserialize("%s/integrator.xml"%run_dir)
            #make sure its the right type of force
            assert(type(system.getForce(6)))==mm.openmm.CustomBondForce
            new_f = system.getForce(6)
            #make sure its the right functional form 
            assert(new_f.getEnergyFunction()=="step(r-r0) * (k/2) * (r-r0)^2")
            #get the bond params
            print new_f.getBondParameters(0)
            #make srue there is only 1 instance of it and that we have the right restraints of 4.5nm and 100kJ/mol
            assert(new_f.getNumBonds()==1)
            assert(new_f.getBondParameters(0)[2]==(4.5,100))
