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
