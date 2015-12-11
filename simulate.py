import os 
from simtk.openmm.app import *
from simtk.openmm import *
from simtk.unit import *
from sys import stdout
import optparse
from add_restraint import *

def serializeObject(i,obj,objname):
    filename = './RUN'+str(i)+'/'+objname
    objfile = open(filename,'w')
    objfile.write(XmlSerializer.serialize(obj))
    objfile.close()


def run(kinase,ptop,crd,i,d):
    if os.path.isfile("./RUN%s/state0.xml%i") and os.stat("./RUN%s/state0.xml"%i).st_size != 0 \
and os.path.isfile("./RUN%s/%s.pdb"%(i,i)) and os.stat("./RUN%s/%s.pdb"%(i,i)).st_size != 0 :
	return
    else:
        platform = Platform.getPlatformByName("CUDA")
        properties = {'CudaPrecision': 'mixed', 'CudaDeviceIndex': str(d)}
        prmtop = AmberPrmtopFile(ptop)
        inpcrd = AmberInpcrdFile(crd,loadBoxVectors = True)
        box = inpcrd.getBoxVectors()
        #forcefield=ForceField('amber99sbildn.xml','tip3p.xml')
        system = prmtop.createSystem(nonbondedMethod=PME, nonbondedCutoff=1*nanometer, constraints=HBonds)
        system.setDefaultPeriodicBoxVectors(box[0],box[1],box[2])
        # Langevin ntt=3, gamma_ln=1.0 
        integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
        integrator.setConstraintTolerance(1e-5)
        #pres0=1.0, ntp=1, taup=2.0,
        system.addForce(MonteCarloBarostat(1*bar, 300*kelvin))
        #add restraints between heavy atoms nearest the center of mass
        add_restrain(kinase,system)

        simulation = Simulation(prmtop.topology, system, integrator,platform,properties)
        simulation.context.setPositions(inpcrd.positions)
        
        
        #simulation.minimizeEnergy()
        simulation.context.setVelocitiesToTemperature(300)
        if not os.path.isdir('RUN'+str(i)):
            os.mkdir('RUN'+str(i))
        f = open("RUN"+"%s/statedata-%s.log" %(i,i), 'w', 0)
        simulation.reporters.append(app.PDBReporter("RUN%d/%d.pdb"%(int(i),int(i)),500000)) 
        simulation.reporters.append(app.StateDataReporter(f, 2000,speed=True,step=True, time=True, potentialEnergy=True, totalEnergy=True, temperature=True,separator='\t'))
        #running 1ns of simulation 
        simulation.step(10)
        #simulation.step(500000)
        state=simulation.context.getState(getPositions=True, getVelocities=True, getForces=True,getEnergy=True,getParameters=True,enforcePeriodicBox=True)
        serializeObject(i,state,'state0.xml')
        serializeObject(i,system,'system.xml')
        serializeObject(i,integrator,'integrator.xml')
        for clone in range(1,6):
            system.getForce(5).setRandomNumberSeed(random.randint(-100000000,100000000))
            integrator.setRandomNumberSeed(random.randint(-100000000,100000000))
            simulation.context.setVelocitiesToTemperature(300*unit.kelvin)
            simulation.step(1)
            new_state=simulation.context.getState(getPositions=True, getVelocities=True,getForces=True,getEnergy=True,getParameters=True,enforcePeriodicBox=True)
            serializeObject(run,new_state,'state%d.xml'%clone)
    return 

def parse_cmdln():
    import os
    parser=optparse.OptionParser()
    parser.add_option('-k','--kinase',dest='k',type='string')
    parser.add_option('-p','--prmtop',dest='ptop',type='string')
    parser.add_option('-c','--crd',dest='crd',type='string')
    parser.add_option('-i','--run',dest='i',type='string')
    parser.add_option('-d','--device',dest='d',type='string')
    (options, args) = parser.parse_args()
    return (options, args)

if __name__=="__main__":
    (options,args)=parse_cmdln()
    run(options.k,options.ptop,options.crd,options.i,options.d)

