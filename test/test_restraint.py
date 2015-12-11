#!/bin/env python

'''
Make sure we state/system/integrator xmls have the necessary extra restraint
'''


state=""
system=""
integrator=0
assert(type(system.getForce(6)))==simtk.openmm.openmm.CustomBondForce
