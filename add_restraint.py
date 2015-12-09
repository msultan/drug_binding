#!/bin/env python


import simtk.openmm as mm
import mdtraj as mdt
import numpy as np

def get_atoms_nearest_centroid(kinase,run_index=0):
    t=mdt.load("./%s_models/%d/%s.pdb"%(kinase,run_index,kinase))

    protein_slice = t.atom_slice([i.index for i in t.top.atoms if i.residue.is_protein and i.element.name!="hydrogen"])
    drug_slice = t.atom_slice([i.index for i in t.top.atoms if i.residue.name=='LIG'])


    prot_com = mdt.compute_center_of_mass(protein_slice)
    drug_com = mdt.compute_center_of_mass(drug_slice)



    prot_atom_index =  np.argmin([np.linalg.norm(t.xyz[:,a.index,:]-prot_com) 
                                     for a in t.top.atoms])
    #since we need to limit to drug, i slice and then add back 
    drug_atom_index =  np.argmin([np.linalg.norm(t.xyz[:,a.index,:] - drug_com) \
                                         for a in t.top.atoms if a.residue.name=='LIG']) + protein_slice.n_atoms
    
    assert(t.top.atom(prot_atom_index).residue.is_protein)
    assert(t.top.atom(drug_atom_index).residue.name=="LIG")
    distance_between_atoms = mdt.compute_distances(t,[[prot_atom_index,drug_atom_index]])
    return prot_atom_index,drug_atom_index,distance_between_atoms


def add_contrainst(kinase, system):
    protein_ind,drug_ind,distance = get_atoms_nearest_centroid(kinase)

    flat_bottom_force = mm.CustomBondForce('step(r-r0) * (k/2) * (r-r0)^2')
    flat_bottom_force.addPerBondParameter('r0', 8.0)
    flat_bottom_force.addPerBondParameter('k', 1.0)

    system.addForce(flat_bottom_force)
    return system 

