"""
From ChatGPT
"""



import SimpleITK as sitk
import matplotlib.pyplot as plt

# Specify the path to the DICOM directory
dicom_dir = "C:\\Users\\esthe\\OneDrive\\Desktop\\Mastergrad\\test1\\files2\\files"

# Load the DICOM series
reader = sitk.ImageSeriesReader()
dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
reader.SetFileNames(dicom_names)
image = reader.Execute()

# Get the image array
image_data = sitk.GetArrayFromImage(image)

# Get image information
spacing = image.GetSpacing()
size = image.GetSize()
origin = image.GetOrigin()

print("Image size:", size)
print("Image spacing:", spacing)
print("Image origin:", origin)

print(image_data[5])

plt.imshow(image_data[5], cmap=plt.cm.gray)
plt.show()