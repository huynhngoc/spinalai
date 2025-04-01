import h5py
import SimpleITK as sitk
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_name', type=str, required=True)
    folder_name = parser.parse_args().folder_name

    folder_path = f'../perf/{folder_name}'
    nifti_path = f'../cropped_nifti_by_soft_tissue_window'

    with h5py.File(f'{folder_path}/predictions.h5', 'r') as f:
        for key in f['predicted'].keys():
            print('Processing', key)
            sitk_image = sitk.ReadImage(f'{nifti_path}/{key}/roi.nii.gz')
            original_y, original_x = list(sitk_image.GetSize())[:2]
            image = sitk.GetImageFromArray(f['predicted'][key][:, :original_x, :original_y])
            image.CopyInformation(sitk_image)
            output_roi_nifti_file = f'{nifti_path}/{key}/{folder_name.replace("_all", "")}_pred.nii.gz'
            sitk.WriteImage(image, output_roi_nifti_file)
            print(f'{key} done')
