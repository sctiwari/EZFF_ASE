import os, sys
import glob
lib_path = os.path.abspath(os.path.join('../..'))
sys.path.append(lib_path)
import ezff
from ezff.interfaces import gulp, qchem, vasp 
from ezff.utils.reaxff import reax_forcefield
from ezff.utils import convert_units as convert
import time

# Define ground truths
gt_gs = vasp.read_atomic_structure("ground_truths/OUTCAR")                            
gt_gs_energy = vasp.read_energy_outcar('ground_truths/OUTCAR') 
print(gt_gs.snaplist[0].atomlist)

outfiles = glob.glob('ground_truths/*.out')
qgt_gs = qchem.read_structure(outfiles)
qgt_gs_energy = qchem.read_energy(outfiles)
qgt_gs_charges = qchem.read_atomic_charges(outfiles)
print(qgt_gs.snaplist[0].atomlist)
