
# library imports
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

bone_0005 = [0.940, 0.935, 0.886, 0.913, 0.912, 0.946, 0.862]
bone_001 = [0.940, 0.933, 0.878, 0.913, 0.926, 0.950, 0.892]
bone_0001 = []
soft_tissue_0005 = [0.924, 0.930, 0.797, 0.924, 0.949, 0.956, 0.745]
soft_tissue_001 = [0.947, 0.904, 0.858, 0.887, 0.806, 0.922, 0.929]
soft_tissue_0001 = []
combine_0005 = [0.940, 0.935, 0.886, 0.913, 0.912, 0.946, 0.862]
combine_001 = [0.940, 0.933, 0.878, 0.913, 0.926, 0.950, 0.892]
combine_0001 = []

# Data from ensemble
f1_3 = [0.913, 0.887, 0.912, 0.924, 0.925, 0.915, 0.944, 0.941, 0.940]
f1_16 = [0.878, 0.858, 0.935, 0.797, 0.897, 0.841, 0.914, 0.882, 0.851]
f1_43 = [0.926, 0.806, 0.946, 0.949, 0.935, 0.955, 0.954, 0.953, 0.948]
f1_51 = [0.950, 0.922, 0.862, 0.956, 0.937, 0.958, 0.950, 0.953, 0.951]
f1_56 = [0.892, 0.929, 0.886, 0.745, 0.893, 0.880, 0.739, 0.797, 0.897]
f1_107 = [0.940, 0.947, 0.940, 0.924, 0.930, 0.928, 0.948, 0.939, 0.953]
f1_111 = [0.933, 0.904, 0.913, 0.930, 0.926, 0.877, 0.943, 0.927, 0.951]


# Sample data
data = {
    'Sample-ID': ['3'] * 9+ ['16'] * 9+ ['43'] * 9+ ['51'] * 9+ ['56'] * 9+ ['107'] * 9+ ['111'] * 9,
    'Dice-score':  f1_3 + f1_16 + f1_43 + f1_51 + f1_56 + f1_107 + f1_111,
    }

# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
sns.violinplot(x='Sample-ID', y='Dice-score', data=df, color="lightgray", cut=0)

# Overlay the data points
sns.swarmplot(x='Sample-ID', y='Dice-score', data=df, alpha=0.6, dodge=True)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'f1_pid.png')
plt.savefig(output_path, dpi=300)
plt.show()

