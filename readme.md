Then, you can install the required packages by running the following command:
```bash
pip install -r requirements.txt
```


# Building the singularity container

```
sbatch slurm_build_singularity.sh <container name> <definition file>
```

For example
```
sbatch slurm_build_singularity.sh deoxys.sif Singularity
```
You can build your own singularity file with additional library by updating the `Singularity` file. Remember to keep an backup of the original `deoxys.sif`.


# Running an interactive python session
After logging into Orion,
```
qlogin --constraint=avx2 --mem=16G
singularity exec --nv deoxys.sif ipython
```
Use this to test your code before committing on your local PC.
Remember to `exit` the session (twice) after you finish.
Note that a `qlogin` session will stop automatically after a while.

```
qlogin --partition gpu --gres gpu:1 --mem 16G
```


# Running a python file
```
sbatch slurm_run_python_file.sh <path_to_file> <optional: parameters>
```
## Example
### Running the cropping script
```
sbatch slurm_run_python_file.sh data_gen/crop_by_soft_tissue.py
```
This script takes no parameter.

### Running the data analysis script
```
sbatch slurm_run_python_file.sh data_gen/data_analysis.py --folder_name cropped_nifti_by_soft_tissue_window
```

This script takes one named parameter (`folder_name`) with the value of `cropped_nifti_by_soft_tissue_window`.
According the the python file, this script will browse the folder with the name `cropped_nifti_by_soft_tissue_window` in the top-level folder (`SpinalAI/`) and save a csv file containing the information of the nifti files in that folder.

### Running the h5_file script
```
sbatch slurm_run_python_file.sh data_gen/generate_h5_file.py --nifti_folder ../cropped_nifti_by_soft_tissue_window --h5_filename ../datasets/spinal_soft_tissue_cropped.h5 --size_0 512 --size_1 512
```

This script takes 4 arguments (parameters):
- The path to the cropped nifti folder (`nifti_folder`)
- The path and filename to the output h5 file (`h5_filename`)
- The size of the x axis `size_0`
- The size of the y axis `size_1`

Actually, the last two arguments are set to 512 by default, so you can skip them.

### Running the ensemble script
```
sbatch slurm_run_python_file.sh post_process/ensemble.py soft_tissue_lr001_{folds}
```
This script will ensemble posible results from the experiment with the prefix `soft_tissue_lr001_` and save the ensemble results in `../perf/soft_tissue_lr001_all`.

To run this script for other experiment, simply replace `soft_tissue_lr001_{folds}` with the corresponding names.
For example, replace it with `soft_tissue_lr001_{folds}_narrow_window`

### Running the result analysis script
```
sbatch slurm_run_python_file.sh analysis/compare_volumes.py soft_tissue_lr001_{folds}
```
This script will calculate the total 3D volumes created by the CNN models and save them in `../analysis_results/soft_tissue_lr001_all`. NOTE: The ensemble script must be run first before this analysis script is run.

To run this script for other experiment, simply replace `soft_tissue_lr001_{folds}` with the corresponding names.
For example, replace it with `soft_tissue_lr001_{folds}_narrow_window`


# Running the experiment

## Running the experiment locally

```
python experiment.py config/local/soft_tissue_lr001.json P:/SpinalAI/test_perf --epoch 2
```

## Running the experiments on Orion
```
sbatch slurm_run_experiment.sh config/soft_tissue_lr001_f012.json soft_tissue_lr001_f012 60
```

This will run the experiment based on the `config/soft_tissue_lr001_f012.json` configuration for 60 epochs, and save the data to the `soft_tissue_lr001_f012` in the `../perf` folder. By default, models and predictions are saved every 5 epochs. To change that, you can add other options using

```
sbatch slurm_run_experiment.sh config/soft_tissue_lr001_f012.json soft_tissue_lr001_f012 60 --model_checkpoint_period 1 --prediction_checkpoint_period 1
```
