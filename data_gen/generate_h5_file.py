import h5py
import SimpleITK
import numpy as np
import argparse

# region Split the data into folds


def create_folds():
    pids = [107, 111, 16, 3, 43, 51, 56]
    slice_numbers = [243, 205, 160, 461, 558, 177, 405]

    # Number of folds
    num_fold = 3

    # Sort the slice numbers in descending order
    sorted_slice_numbers = sorted(
        enumerate(slice_numbers), key=lambda x: x[1], reverse=True)

    # Initialize the folds
    fold_indice = [[] for _ in range(num_fold)]
    fold_sizes = [0] * num_fold

    # Distribute the slice numbers into the folds
    for idx, size in sorted_slice_numbers:
        # Find the fold with the smallest total size
        min_index = np.argmin(fold_sizes)
        # Add the slices of the patients to this fold
        fold_indice[min_index].append(idx)
        # Update the total size of this fold
        fold_sizes[min_index] += size

    # Print the distribution
    for i, group in enumerate(fold_indice):
        print(f"fold {i+1}: {group}, Total Size: {fold_sizes[i]}")

    folds = [np.array(pids)[fold_index].tolist() for fold_index in fold_indice]
    return folds
# endregion Split the data into folds


def load_image(patient_id, nifti_folder):
    image_path = f'{nifti_folder}/{patient_id}/image.nii.gz'
    return SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(image_path))


def load_target(patient_id, nifti_folder):
    target_path = f'{nifti_folder}/{patient_id}/roi.nii.gz'
    return SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(target_path))


def pad_image(image, target, desired_shape):
    desired_shape = [image.shape[0]] + list(desired_shape)
    image_shape = image.shape
    pad_shape = [(0, desired_shape[i] - image_shape[i]) for i in range(3)]
    image = np.pad(image, pad_shape, mode='constant',
                   constant_values=image.min())
    target = np.pad(target, pad_shape, mode='constant', constant_values=0)
    return image, target


def print_h5_file_structure(file_path):
    with h5py.File(file_path, 'r') as h5_file:
        for key in h5_file.keys():
            print(key)
            for sub_key in h5_file[key].keys():
                print(f'  {sub_key}', h5_file[key][sub_key])


if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--nifti_folder', type=str, required=True)
    argparse.add_argument('--h5_filename', type=str, required=True)
    argparse.add_argument('--size_0', type=int, default=512)
    argparse.add_argument('--size_1', type=int, default=512)

    args = argparse.parse_args()

    nifti_folder = args.nifti_folder
    h5_filename = args.h5_filename
    size_0 = argparse.size_0
    size_1 = argparse.size_1

    folds = create_folds()

    with h5py.File(h5_filename, 'w') as h5_file:
        for fold_idx, fold in enumerate(folds):
            group = h5_file.create_group(f'fold_{fold_idx}')

            patient_indices = []
            slice_indices = []
            images = []
            targets = []

            for patient_id in fold:
                image_slices = load_image(patient_id)
                print(image_slices.shape)
                target_slices = load_target(patient_id)
                print(target_slices.shape)

                padded_image_slices, padded_target_slices = pad_image(
                    image_slices, target_slices, (size_0, size_1))

                num_slices = image_slices.shape[0]
                patient_indices.extend([patient_id] * num_slices)
                slice_indices.extend(list(range(num_slices)))
                images.append(padded_image_slices)
                targets.append(padded_target_slices)

            images = np.concatenate(images, axis=0)
            targets = np.concatenate(targets, axis=0)

            group.create_dataset('patient_idx', data=np.array(patient_indices))
            group.create_dataset('slice_idx', data=np.array(slice_indices))
            group.create_dataset('image', data=images, dtype=np.float32)
            group.create_dataset('target', data=targets)

    print_h5_file_structure(h5_filename)
