import h5py
import SimpleITK as sitk
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_name', type=str, required=True)
    folder_name = parser.parse_args().folder_name

    folder_path = f'../perf/{folder_name}'
    nifti_path = f'../cropped_nifti_by_soft_tissue_window/'

    with h5py.File(f'{folder_path}/predictions.h5', 'r') as f:
        for key in f.keys():
            print('Processing', key)
            sitk_image = sitk.ReadImage(f'{nifti_path}/{key}/roi.nii.gz')
            image = sitk.GetImageFromArray(f[key]['predicted'][:])
            image.CopyInformation(sitk_image)
            output_roi_nifti_file = f'{nifti_path}/{key}_{folder_name.replace('_all','')}_pred.nii.gz'
            sitk.WriteImage(output_roi_nifti_file, output_roi_nifti_file)
            print(f'{key} done')
