import os, sys
import glob
lib_path = os.path.abspath(os.path.join('../..'))
sys.path.append(lib_path)
import ezff
from ezff.interfaces import gulp, qchem, vasp 
from ezff.utils.reaxff import reax_forcefield
from ezff.utils import convert_units as convert
import time


print(ezff.__path__)
# Define ground truths
gt_gs = vasp.read_atomic_structure("ground_truths/OUTCAR")                            
gt_gs_energy = vasp.read_energy_outcar('ground_truths/OUTCAR') 
print(gt_gs.box)



def my_error_function(rr):
    # Get a unique path for GULP jobs from the MPI rank. Set to '0' for serial jobs
    try:
        path = str(pool.rank)
    except:
        path = '0'

    # Calculate Ground State
    md_gs_job = gulp.job(verbose=True, path = path)
    md_gs_job.structure = gt_gs
    md_gs_job.forcefield = ezff.generate_forcefield(template, rr, FFtype = 'reaxff')
    md_gs_job.options['pbc'] = True
    md_gs_job.options['relax_atoms'] = False
    md_gs_job.options['relax_cell'] = False
    # Run GULP calculation
    md_gs_job.run(command='gulp')
    # Read output from completed GULP job and clean-up
    md_gs_energy = md_gs_job.read_energy()
    print (md_gs_energy)
    md_gs_job.cleanup()

    # Calculate error
    energy_error = ezff.error_energy(md_gs_energy, gt_gs_energy, weights = 'uniform')
    print(energy_error)
    return [energy_error]


pool = ezff.Pool()

if pool.is_master():
    # Generate forcefield template and variable ranges
    FF = reax_forcefield('ffield')
    FF.make_template_twobody('ZR','S', double_bond=True)
    FF.make_template_twobody('ZR','O', double_bond=False)
    FF.generate_templates()

time.sleep(5.0)

# Read template and variable ranges
bounds = ezff.read_variable_bounds('param_ranges', verbose=False)
template = ezff.read_forcefield_template('ff.template.generated')
time.sleep(5.0)
problem = ezff.OptProblem(num_errors = 1, variable_bounds = bounds, error_function = my_error_function, template = template)
algorithm = ezff.Algorithm(problem, 'NSGAII', population = 2, pool = pool)
ezff.optimize(problem, algorithm, iterations = 1, write_forcefields = 1)
pool.close()
