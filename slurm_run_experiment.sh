#!/bin/bash
# SBATCH --ntasks=1               # 1 core(CPU)
# SBATCH --nodes=1                # Use 1 node
# SBATCH --job-name=SpinalAI_run   # sensible name for the job
# SBATCH --mem=64G                 # Default memory per CPU is 3GB.
# SBATCH --partition=gpu        # Use the GPU partition
# SBATCH --gres=gpu:1       # Request 1 GPU "generic resource"
# SBATCH --cpus-per-task=16
# SBATCH --mail-user=$USER@nmbu.no # Email me when job is done.
# SBATCH --mail-type=ALL
# SBATCH --output=outputs/unet-%A.out
# SBATCH --error=outputs/unet-%A.out

# If you would like to use more please adjust this.

# Below you can put your scripts
# If you want to load module
module load singularity

# Code (skipped because the SSD seems full)
# If data files aren't copied, do so
#!/bin/bash
# if [$  # -lt 3 ];
#     then
#     printf "Not enough arguments - %d\n" $
#     exit 0
#     fi

# if [! -d "$TMPDIR/$USER/hn_delin"]
#     then
#     echo "Didn't find dataset folder. Copying files..."
#     mkdir - -parents $TMPDIR /$USER/hn_delin
#     fi

# for f in $(ls $HOME/datasets/headneck/*)
#     do
#     FILENAME =`echo $f | awk - F / '{print $NF}'`
#     echo $FILENAME
#     if [! -f "$TMPDIR/$USER/hn_delin/$FILENAME"]
#         then
#         echo "copying $f"
#         cp - r $HOME/datasets/headneck /$FILENAME $TMPDIR /$USER/hn_delin /
#         fi
#     done


echo "Finished seting up files."

# Hack to ensure that the GPUs work
nvidia-modprobe -u -c=0

# Run experiment
# export ITER_PER_EPOCH=200
export MAX_SAVE_STEP_GB=0
export NUM_CPUS=4
export RAY_ROOT =$TMPDIR/ray
singularity exec - -nv deoxys.sif python experiment.py $1 $PROJECTS/ngoc/SpinalAI/perf/$2 - -temp_folder $SCRATCH_PROJECTS/ceheads/SpinalAI/perf/$2 - -analysis_folder $SCRATCH/analysis/$2 --epochs $3 ${@: 4}
