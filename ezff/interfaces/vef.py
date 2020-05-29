#!/usr/bin/env python
import aselite
from os.path import isfile, dirname, abspath, join
from os import system
from sys import exit, argv

if '-h' in argv:
    print('usage: vef.py')
    print('       prints the force and energy for each ionic step of a vasp run')
    print('')
    exit(0)

vtst_path = dirname(abspath(__file__))

filename = 'OUTCAR'
if not isfile(filename):
    print('No such file: %s' % filename)
    exit(1)

traj = aselite.read_vasp_out(filename)
if len(traj) == 0:
    exit(0)

for i, Atoms in enumerate(traj):
    Atoms.write("config.xyz",'xyz')
    print( Atoms.get_chemical_symbols(), Atoms.get_positions())
#aselite.write_xyz("config.xyz",traj)
