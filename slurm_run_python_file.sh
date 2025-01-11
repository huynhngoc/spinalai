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
#SBATCH --error=outputs/pretrain-%A.out

# If you would like to use more please adjust this.

## Below you can put your scripts
# If you want to load module
module load singularity


# Hack to ensure that the GPUs work
nvidia-modprobe -u -c=0

singularity exec --nv deoxys.sif python $1 ${@:2}
