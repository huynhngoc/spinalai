import os
import pandas as pd
import SimpleITK as sitk


def get_nifti_info(file_path):
    image = sitk.ReadImage(file_path)
    spacing = image.GetSpacing()
    origin = image.GetOrigin()
    direction = image.GetDirection()
    size = image.GetSize()
    return spacing, origin, direction, size


def analyze_nifti_files(folder_path):
    data = []
    for pid in os.listdir(folder_path):
        for file_name in os.listdir(os.path.join(folder_path, pid)):
            if file_name == 'image.nii' or file_name == 'image.nii.gz':
                file_path = os.path.join(folder_path, pid, file_name)
                spacing, origin, direction, size = get_nifti_info(file_path)
                data.append([pid, file_name, spacing, origin, direction, size])
            if file_name == 'roi.nii' or file_name == 'roi.nii.gz':
                file_path = os.path.join(folder_path, pid, file_name)
                spacing, origin, direction, size = get_nifti_info(file_path)
                data.append([pid, file_name, spacing, origin, direction, size])

    df = pd.DataFrame(
        data, columns=['PID', 'FileName', 'Spacing', 'Origin', 'Direction', 'Size'])
    return df


folder_path = 'P:/SpinalAI/cropped_nifti_by_soft_tissue_window/'
output_csv = 'P:/SpinalAI/cropped_nifti_by_soft_tissue_window_info.csv'


df = analyze_nifti_files(folder_path)

df.to_csv(output_csv, index=False)
