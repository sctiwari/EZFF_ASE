#!/bin/bash
#SBATCH --ntasks=64
#SBATCH --time=120:00:00
#SBATCH -p priya
#SBATCH --output=out1
#SBATCH --job-name=RXFF-ZrOS

source /usr/usc/intel/18.1/setup.sh
export PATH=~/hpc/software/gulp-5.2/bin:$PATH
source /auto/hpc-23/sctiwari/software/conda/etc/profile.d/conda.sh
conda activate base

srun -n 64 --mpi=pmi2 python3.7 run.py

exit 0
