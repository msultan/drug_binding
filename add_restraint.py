#!/bin/env python


import simtk.openmm as mm
import mdtraj as mdt
import numpy as np

def get_atoms_nearest_centroid(kinase,run_index=0):
    t=mdt.load("/home/msultan/research/kinase/drug_binding/2016/drug_binding/%s_models/%d/prot.pdb"%(kinase,run_index))
    
    all_protein_slice = t.atom_slice([i.index for i in t.top.atoms if i.residue.is_protein])
    protein_slice = t.atom_slice([i.index for i in t.top.atoms if i.residue.is_protein and i.element.name!="hydrogen"])
    drug_slice = t.atom_slice([i.index for i in t.top.atoms if i.residue.name=='LIG'])


    prot_com = mdt.compute_center_of_mass(protein_slice)
    drug_com = mdt.compute_center_of_mass(drug_slice)



    prot_atom_index =  np.argmin([np.linalg.norm(t.xyz[:,a.index,:]-prot_com) 
                                     for a in t.top.atoms])
    #since we need to limit to drug, i slice and then add back 
    drug_atom_index =  np.argmin([np.linalg.norm(t.xyz[:,a.index,:] - drug_com) \
                                         for a in t.top.atoms if a.residue.name=='LIG']) + all_protein_slice.n_atoms
    
    assert(t.top.atom(prot_atom_index).residue.is_protein)
    assert(t.top.atom(drug_atom_index).residue.name=="LIG")
    distance_between_atoms = mdt.compute_distances(t,[[prot_atom_index,drug_atom_index]])
    return prot_atom_index,drug_atom_index,distance_between_atoms


def add_restrain(kinase, system):
    protein_ind,drug_ind,distance = get_atoms_nearest_centroid(kinase)
    
    print protein_ind,drug_ind,distance

    distance_param = 4.5 * mm.unit.nanometers
    force_constant_param = 100 * mm.unit.kilojoules_per_mole/ mm.unit.nanometers**2 
      
    flat_bottom_force = mm.CustomBondForce('step(r-r0) * (k/2) * (r-r0)^2')
    flat_bottom_force.addPerBondParameter('r0')
    flat_bottom_force.addPerBondParameter('k')

    system.addForce(flat_bottom_force)
    flat_bottom_force.addBond(protein_ind, drug_ind, [distance_param, force_constant_param])
    return system 

