#!/bin/bash
#SBATCH --ntasks=1               # 1 core(CPU)
#SBATCH --nodes=1                # Use 1 node
#SBATCH --job-name=SpinalAI_run   # sensible name for the job
#SBATCH --mem=16G                 # Default memory per CPU is 3GB.
#SBATCH --partition=orion         # Use hugemem if you need > 48 GB (check the orion documentation)
#SBATCH --constraint=avx2
#SBATCH --mail-user=$USER@nmbu.no # Email me when job is done.
#SBATCH --mail-type=FAIL
#SBATCH --output=outputs/run_python-%A.out
#SBATCH --error=outputs/run_python-%A.out

module load singularity

singularity build --fakeroot $1 $2
