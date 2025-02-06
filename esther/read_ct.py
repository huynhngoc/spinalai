import nibabel as nib

def read_nifti_file(file_path):
    # Load the NIfTI file
    nifti_img = nib.load(file_path)
    
    # Get the data from the NIfTI file
    data = nifti_img.get_fdata()
    
    return data

# Example usage
file_path = 'path_to_your_nifti_file.nii'
nifti_data = read_nifti_file(file_path)
print(nifti_data.shape)