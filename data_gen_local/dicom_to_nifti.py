import pydicom
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import os
from skimage.draw import polygon
import json

# Path to the DICOM series directory
dicom_dir = "P:/SpinalAI/Some example images/Studies with ROIs/"
output_dir = "P:/SpinalAI/nifti/"

os.listdir(dicom_dir)
i = 4
patient_folder_name = os.listdir(dicom_dir)[i]


# Read the DICOM series using SimpleITK
def find_dicom_series(dicom_dir):
    reader = sitk.ImageSeriesReader()
    for root, dirs, files in os.walk(dicom_dir):
        for dir_name in dirs:
            patient_folder = os.path.join(root, dir_name)
            dicom_names = reader.GetGDCMSeriesFileNames(patient_folder)
            if dicom_names:
                # series_IDs = sitk.ImageSeriesReader.GetGDCMSeriesIDs(patient_folder)
                return dicom_names, patient_folder
    return None, None


dicom_names, patient_folder = find_dicom_series(
    os.path.join(dicom_dir, patient_folder_name))
print('Found the Dicom series in:', patient_folder,
      'with', len(dicom_names), 'files')
print('Reading the Dicom series...')

reader = sitk.ImageSeriesReader()
reader.SetFileNames(dicom_names)
reader.SetImageIO("GDCMImageIO")
image = reader.Execute()

# Get spacing information from DICOM metadata
first_file = dicom_names[0]
ds = pydicom.dcmread(first_file)

origin = ds.ImagePositionPatient
spacing = list(ds.PixelSpacing) + [float(ds.SliceThickness)]
dicom_direction = ds.ImageOrientationPatient
direction = np.concatenate(
    [dicom_direction, np.cross(dicom_direction[:3], dicom_direction[3:])])

image.SetOrigin(origin)
image.SetSpacing(spacing)
image.SetDirection(direction)

image_data = sitk.GetArrayFromImage(image)
roi_data = np.zeros_like(image_data)
# Read the ROI data from the private tag
roi_private_tag = (0x5000, 0x3000)
roi_points = []
print('Reading the ROI data...')
for i, dicom_file in enumerate(dicom_names):
    print(i)
    ds = pydicom.dcmread(dicom_file)
    roi_binary_data = ds[roi_private_tag].value
    contour_points = np.frombuffer(
        roi_binary_data, dtype=np.float32).reshape(-1, 2)
    rr, cc = polygon(
        contour_points[:, 1], contour_points[:, 0], shape=image_data.shape[1:])
    roi_data[i][rr, cc] = 1
    roi_points.append(contour_points)

# Create a SimpleITK image from the ROI data
roi_image = sitk.GetImageFromArray(roi_data)

# Set the origin, spacing, and direction of the ROI image to match the original image
roi_image.SetOrigin(image.GetOrigin())
roi_image.SetSpacing(image.GetSpacing())
roi_image.SetDirection(image.GetDirection())

print('Saving the Nifti files...')
# Save the ROI image as a NIfTI file
os.makedirs(os.path.join(
    output_dir, patient_folder_name.split('(')[0]), exist_ok=True)

output_roi_nifti_file = os.path.join(
    output_dir, patient_folder_name.split('(')[0], 'roi.nii.gz')
output_image_nifti_file = os.path.join(
    output_dir, patient_folder_name.split('(')[0], 'image.nii.gz')
sitk.WriteImage(image, output_image_nifti_file)
sitk.WriteImage(roi_image, output_roi_nifti_file)

roi_points_list = [points.tolist() for points in roi_points]
output_json_file = os.path.join(
    output_dir, patient_folder_name.split('(')[0], 'roi_points.json')
with open(output_json_file, 'w') as json_file:
    json.dump(roi_points_list, json_file)

# plt.figure(figsize=(10, 10))
# plt.subplot(2, 2, 1)
# plt.imshow(image_data[0], cmap='gray')
# plt.plot(roi_points[0][:, 0], roi_points[0][:, 1], 'r-', linewidth=2)
# plt.subplot(2, 2, 2)
# plt.imshow(image_data[0], cmap='gray')
# plt.contour(roi_data[0], levels=[0.5], colors='r', linewidths=2)
# plt.subplot(2, 2, 3)
# plt.imshow(roi_data[0], cmap='gray', alpha=0.5)
# plt.subplot(2, 2, 4)
# plt.imshow(image_data[0], cmap='gray')
# plt.plot(roi_points[0][:, 0], roi_points[0][:, 1], 'r-', linewidth=2)
# plt.contour(roi_data[0], levels=[0.5], colors='b', linewidths=2)
# plt.show()
