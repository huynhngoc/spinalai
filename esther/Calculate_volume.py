import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
import pandas as pd
import json
import os 


def polygon_area(points):
    points = np.asarray(points)
    x = points[:, 0]
    y = points[:, 1]
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

pid = 111

# File path for the image
pid_path = 'data/' + str(pid)
roi_path = pid_path + '/roi.nii.gz'

# Read the image
roi = sitk.ReadImage(roi_path)
roi_array = sitk.GetArrayFromImage(roi)

print(roi_array.shape)
slice1 = roi_array[150]

plt.imshow(slice1, cmap='gray')
plt.show()

# calculate the volume of the ROI based on Voxels
print(roi.GetSpacing())
voxel_size = np.prod(roi.GetSpacing())
print(voxel_size)

volume_of_voxels = np.sum(slice == 1) * voxel_size

volume_list = []
for slice in roi_array:
    print(slice.shape)
    volume_of_voxels = np.sum(slice == 1) * voxel_size
    print(volume_of_voxels)
    volume_list.append(volume_of_voxels)
    #plt.imshow(slice, cmap='gray')
    #plt.show()

# Calculate the actual volume using the ROI points
voxel_area = np.prod(roi.GetSpacing()[:2])  # Calculate the area of a single voxel (x and y spacing)
slice_thickness = roi.GetSpacing()[2]  # Get the slice thickness
actual_volume = []

with open(os.path.join(pid_path, 'roi_points.json'), 'r') as f:
    rois_per_slice = json.loads(f.read())

# Iterate through each slice and apply the ROIs
for roi_points in rois_per_slice:
    area_of_rois = polygon_area(roi_points) * voxel_area
    volume_of_slice = area_of_rois * slice_thickness
    actual_volume.append(volume_of_slice)

# Create a DataFrame with column titles
df = pd.DataFrame({'Slice_Index': range(len(volume_list)), 'Volume': volume_list, 'Actual_Volume': actual_volume})

print(df)

# File path for the CSV file
csv_file_path = 'outputs//volume_'+str(pid)+'.csv'

# Write the DataFrame to a CSV file with column titles and row numbers
df.to_csv(csv_file_path, index=False)