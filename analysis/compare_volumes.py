import pandas as pd
import numpy as np
import os
import SimpleITK as sitk
import json
import h5py
import argparse


def polygon_area(points):
    points = np.asarray(points)
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str)
    experiment_name = parser.parse_args().name

    # preparing the data`
    patient_folder = '../nifti'
    # experiment_name = 'soft_tissue_lr001_{folds}'
    output_folder = f'../analysis_results/{experiment_name.replace("{folds}", "all")}'
    fold_list = ['f012', 'f102', 'f021', 'f201', 'f120', 'f210']

    os.makedirs(output_folder, exist_ok=True)


    # reading the information from the original data
    pids = os.listdir(patient_folder)

    info = []

    print('Calculating the volumes from the original data...')
    for pid in pids:
        print('Processing patient', pid)
        pid_path = os.path.join(patient_folder, pid)
        roi_filepath = os.path.join(pid_path, 'roi.nii.gz')
        # Read the image
        roi = sitk.ReadImage(roi_filepath)
        roi_array = sitk.GetArrayFromImage(roi)

        # calculate the volume of the ROI based on Voxels
        voxel_size = np.prod(roi.GetSpacing())
        volume_of_voxels = np.sum(roi_array == 1) * voxel_size

        # calculate the volume of the ROI based on the area of the ROI
        voxel_area = np.prod(roi.GetSpacing()[:2])  # Calculate the area of a single voxel (x and y spacing)
        slice_thickness = roi.GetSpacing()[2]  # Get the slice thickness
        actual_volume = 0

        with open(os.path.join(pid_path, 'roi_points.json'), 'r') as f:
            rois_per_slice = json.loads(f.read())

        # Iterate through each slice and apply the ROIs
        for roi_points in rois_per_slice:
            area_of_rois = polygon_area(roi_points) * voxel_area
            volume_of_slice = area_of_rois * slice_thickness
            actual_volume += volume_of_slice

        info.append([int(pid), actual_volume, volume_of_voxels, voxel_size])

    df = pd.DataFrame(info, columns=['pid', 'actual_volume', 'voxel_volume', 'voxel_size']).set_index('pid')
    df.to_csv(os.path.join(output_folder, 'original_data_info.csv'))

    print('calculating the results from experiments...')
    for fold in fold_list:
        experiment_info = []
        log_folder = '../perf/' + experiment_name.format(folds=fold)
        perf_info = pd.read_csv(log_folder + '/test/result.csv', index_col='patient_idx').rename_axis('pid')
        test_file = log_folder + '/test/prediction_test.h5'
        with h5py.File(test_file, 'r') as f:
            group = f['predicted']
            for pid in group.keys():
                predicted = group[str(pid)][:][..., 0]
                segmented_voxels = np.sum(predicted > 0.5)
                experiment_info.append([int(pid), segmented_voxels])
        experiment_df = pd.DataFrame(experiment_info, columns=['pid', 'segmented_voxels']).set_index('pid')
        experiment_df = experiment_df.join(df).join(perf_info)
        experiment_df['segmented_volume'] = experiment_df['segmented_voxels'] * experiment_df['voxel_size']
        experiment_df.to_csv(os.path.join(output_folder, f'{fold}_results.csv'))

    print('calculating the results from ensemble...')
    ensemble_info = []
    log_folder = '../perf/' + experiment_name.format(folds='all')
    perf_info = pd.read_csv(log_folder + '/result.csv', index_col='pid')
    test_file = log_folder + '/predictions.h5'
    with h5py.File(test_file, 'r') as f:
        group = f['predicted']
        for pid in group.keys():
            predicted = group[str(pid)][:][..., 0]
            segmented_voxels = np.sum(predicted > 0.5)
            ensemble_info.append([int(pid), segmented_voxels])
    ensemble_df = pd.DataFrame(ensemble_info, columns=['pid', 'segmented_voxels']).set_index('pid')
    ensemble_df = ensemble_df.join(df).join(perf_info)
    ensemble_df['segmented_volume'] = ensemble_df['segmented_voxels'] * ensemble_df['voxel_size']
    ensemble_df.to_csv(os.path.join(output_folder, 'ensemble_results.csv'))
