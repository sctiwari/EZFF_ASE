import ezff
from ezff.interfaces import gulp, vasp
import numpy as np

bounds = ezff.read_variable_bounds('variable_bounds', verbose=False)
template = ezff.read_forcefield_template('template')

# DEFINE GROUND TRUTHS
gt_bulk_modulus = 1.1236 #GPa
gt_structure = vasp.read_atomic_structure('ground_truths/POSCAR')

def my_error_function(variable_values):
    # Get rank from pool
    try:
        myrank = pool.rank
    except:
        myrank = 0

    # Configure GULP job.
    path = str(myrank)
    md_job = gulp.job(path=path)
    md_job.structure = gt_structure
    md_job.forcefield = ezff.generate_forcefield(template, variable_values, FFtype='SW')
    md_job.options['pbc'] = True
    md_job.options['relax_atoms'] = True
    md_job.options['relax_cell'] = True

    # Submit job and read output
    md_job.run()

    # Calculate errors in lattice constant and elastic modulus
    moduli = md_job.read_elastic_moduli()                                                # 6X6 elastic modulus tensor inside a list of length 1 (for a single input structure)
    md_bulk_modulus = np.mean([moduli[0][i,i] for i in range(3)])                        # Bulk modulus is sum of diagonal elements in moduli[0]
    bulk_modulus_error = np.linalg.norm(md_bulk_modulus - gt_bulk_modulus)               # Error is the L2 norm of deviation from the ground truth value

    md_structure = md_job.read_structure()                                               # Read relaxed structure after optimization
    error_abc, error_ang = ezff.error_lattice_constant(MD=md_structure, GT=gt_structure) # error_abc = error in lattice constants, error_ang = error in lattice angles
    latt_error = np.linalg.norm(error_abc[0])                                            # error in 'a' lattice constant

    return [latt_error, bulk_modulus_error]

pool = ezff.Pool()
problem = ezff.OptProblem(num_errors = 2, variable_bounds = bounds, error_function = my_error_function, template = template)
algorithm = ezff.Algorithm(problem, 'NSGAII', population = 32, pool = pool)
ezff.optimize(problem, algorithm, iterations = 16)
pool.close()
