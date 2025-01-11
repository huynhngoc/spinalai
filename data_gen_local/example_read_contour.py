import pydicom
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import os

# Path to the DICOM series directory
dicom_dir = "P:/SpinalAI/Some example images/Studies with ROIs/"

os.listdir(dicom_dir)
i = 1
patient_folder = os.listdir(dicom_dir)[i]

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


# Path to the DICOM series directory
dicom_dir = "P:/SpinalAI/Some example images/Studies with ROIs/"

dicom_names, patient_folder = find_dicom_series(
    os.path.join(dicom_dir, patient_folder))

reader = sitk.ImageSeriesReader()
reader.SetFileNames(dicom_names)
reader.SetImageIO("GDCMImageIO")
# reader.MetaDataDictionaryArrayUpdateOn()
# reader.LoadPrivateTagsOn()


image = reader.Execute()

# Get spacing information from DICOM metadata
dicom_spacing_str = reader.GetMetaData(0, '0028|0030').strip()
dicom_spacing = [float(val) for val in dicom_spacing_str.split('\\')]
slice_thickness = float(reader.GetMetaData(0, '0018|0050').strip())
dicom_spacing.append(slice_thickness)

print(f"DICOM PixelSpacing: {dicom_spacing[:2]}")
print(f"DICOM SliceThickness: {dicom_spacing[2]}")

# Get origin and direction information from DICOM metadata
dicom_origin_str = reader.GetMetaData(0, '0020|0032').strip()
dicom_origin = [float(val) for val in dicom_origin_str.split('\\')]
print(f"DICOM origin: {dicom_origin}")

dicom_direction_str = reader.GetMetaData(0, '0020|0037').strip()
dicom_direction = [float(val) for val in dicom_direction_str.split('\\')]

# Construct the full 3x3 direction cosines matrix
row1 = np.array(dicom_direction[:3])
row2 = np.array(dicom_direction[3:])
row3 = np.cross(row1, row2)

full_direction = np.concatenate((row1, row2, row3)).tolist()

print(f"DICOM direction: {full_direction}")

# Manually set the spacing, origin, and direction in the SimpleITK image
image.SetSpacing(dicom_spacing)
image.SetOrigin(dicom_origin)
image.SetDirection(full_direction)


# Convert SimpleITK image to numpy array for visualization
image_array = sitk.GetArrayFromImage(image)

# get the roi data

private_tag_value = reader.GetMetaData(0, '5000|3000')
binary_private_tag_value = bytes(private_tag_value, 'utf-8')
roi = np.frombuffer(binary_private_tag_value, dtype=np.float32)

# Read the first DICOM file using pydicom to access the private tag
first_file = dicom_names[0]
ds = pydicom.dcmread(first_file)

# Access the private tag (5000, 3000)
roi_private_tag = (0x5000, 0x3000)
if roi_private_tag in ds:
    roi_binary_data = ds[roi_private_tag].value
    print(f"Private tag {roi_private_tag}: {roi_binary_data}")
    print(f"Array length: {len(roi_binary_data)}")

    # Convert the byte array to a numpy array for easier manipulation
    # Adjust dtype if necessary (e.g., np.float32, np.int16, etc.)
    roi_data_array = np.frombuffer(roi_binary_data, dtype=np.float32)
    print(f"Binary data as numpy array: {roi_data_array}")

    # Assuming the data represents a series of (x, y) points
    contour_points = roi_data_array.reshape(-1, 2)
    print(f"Contour points:\n{contour_points}")

    # Display the first slice with the ROI contour
    fig, ax = plt.subplots(1)
    ax.imshow(image_array[0], cmap='gray')

    # Plot the contour
    x, y = contour_points[:, 0], contour_points[:, 1]
    ax.plot(x, y, 'r-', linewidth=2)

    plt.title('First Slice with ROI Contour')
    plt.show()
else:
    print(f"Private tag {roi_private_tag} not found in the DICOM file.")
