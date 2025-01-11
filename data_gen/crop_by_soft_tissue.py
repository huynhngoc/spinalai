import SimpleITK as sitk
import numpy as np
import os


def window_image(image, window_center, window_width):
    img_min = window_center - window_width // 2
    img_max = window_center + window_width // 2
    windowed_image = np.clip(image, img_min, img_max)
    return windowed_image


def crop_to_soft_tissue(image, window_center, window_width):
    windowed_image = window_image(
        sitk.GetArrayFromImage(image), window_center, window_width)
    non_zero_coords = np.argwhere(
        windowed_image > window_center - window_width // 2)
    min_coords = np.min(non_zero_coords, axis=0)
    max_coords = np.max(non_zero_coords, axis=0) + 1
    size = max_coords - min_coords
    return min_coords, size


if __name__ == '__main__':
    input_dir = '../nifti'
    output_dir = '../cropped_nifti_by_soft_tissue_window'
    window_center = 400
    window_width = 1800

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process all image.nii.gz files in the top-level directories
    for pid in os.listdir(input_dir):
        pid_path = os.path.join(input_dir, pid)
        input_img_filepath = os.path.join(pid_path, 'image.nii.gz')
        input_roi_filepath = os.path.join(pid_path, 'roi.nii.gz')
        output_folder = os.path.join(output_dir, pid)
        os.makedirs(output_folder, exist_ok=True)
        output_img_filepath = os.path.join(output_folder, 'image.nii.gz')
        output_roi_filepath = os.path.join(output_folder, 'roi.nii.gz')

        # Read the image
        image = sitk.ReadImage(input_img_filepath)
        roi = sitk.ReadImage(input_roi_filepath)

        # Crop the image to the soft tissue window
        min_coords, size = crop_to_soft_tissue(
            image, window_center, window_width)

        # Use the RegionOfInterestImageFilter to crop the image
        roi_filter = sitk.RegionOfInterestImageFilter()
        # Reverse the order for SimpleITK
        roi_filter.SetIndex(min_coords[::-1].tolist())
        # Reverse the order for SimpleITK
        roi_filter.SetSize(size[::-1].tolist())
        cropped_image = roi_filter.Execute(image)
        cropped_roi = roi_filter.Execute(roi)

        # Save the cropped image
        sitk.WriteImage(cropped_image, output_img_filepath)
        sitk.WriteImage(cropped_roi, output_roi_filepath)

        print(f"Cropped image saved as {output_img_filepath}")
