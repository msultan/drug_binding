import glob
from simtk.unit import *
import random
import os
from simtk.openmm import *
from simtk.openmm import app


runs = glob.glob("RUN*")
n_clones=8
def serializeObject(i,obj,objname):
    filename = './'+i+'/'+objname
    objfile = open(filename,'w')
    objfile.write(XmlSerializer.serialize(obj))
    objfile.close()


for run in runs:
    print run
    with open("%s/state0.xml"%run) as state_input:
        state = XmlSerializer.deserialize(state_input.read())
    with open("%s/system.xml"%run) as system_input:
        system =  XmlSerializer.deserialize(system_input.read())
    with open("%s/integrator.xml"%run) as integrator_input:
        integrator = XmlSerializer.deserialize(integrator_input.read())
                                                          
                                                              
    platform = openmm.Platform.getPlatformByName('Reference')
    simulation = app.Simulation(state, system, integrator, platform)
    simulation.context.setPositions(state.getPositions())

    for clone in range(1,n_clones):
        system.getForce(5).setRandomNumberSeed(random.randint(-100000000,100000000))
        integrator.setRandomNumberSeed(random.randint(-100000000,100000000))
                           
                                   
        simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
        simulation.step(1)
        new_state=simulation.context.getState(getPositions=True, getVelocities=True,getForces=True,getEnergy=True,getParameters=True,enforcePeriodicBox=True)
        serializeObject(run,new_state,'state%d.xml'%clone)



