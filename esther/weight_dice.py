# Importing libraries
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

# data volume discrepancy from ensemble
bone_001 = [2.48, -7.75, 0.35, -0.09, 10.87, 5.42, -4.94]
bone_0005 = [-3.45, -9.96, -9.59, -5.17, 12.23, 3.96, -4.24]
bone_0001 = [-0.351, -3.031, -1.937, -3.279, 0.944, 2.815, -4.097]
soft_tissue_001 = [-5.34, -25.78, -1.93, -11.67, -1.10, -10.93, -7.81]
soft_tissue_0005 = [0.83, -50.03, 4.47, 2.13, 33.56, -8.89, -10.49]
soft_tissue_0001 = [-10.302, -20.526, 3.376, 2.230, 3.158, -8.430, -25.707]
combine_0001 = [5.341, -14.989, 2.180, 0.532, 44.829, -2.059, -7.891]
combine_0005 = [-1.048, -17.757, -1.330, 0.639, 24.799, 1.630, -12.894]
combine_001 = [5.879, -24.663, 4.585, 5.5604, 3.3114, -4.418, -2.757]

bone_001_mean = np.mean(bone_001)
bone_0005_mean = np.mean(bone_0005)
bone_0001_mean = np.mean(bone_0001)

# Sample data
data = {
    'Sample-ID': ['3', '16', '43', '51', '56', '107', '111']* 9,
    'Weight [kg]': ['37', '2.3', '62.9', '12.2', '27.9', '10.1', '4.8']*9,
    'Relative age to life-span [yrs]' : ['0.229', '0.536', '0.194', '0.111', '0.591', '0.2', '0.310']*9,
    'Volume discrepancy [%]':  bone_001 + bone_0005 + bone_0001 + soft_tissue_001 + soft_tissue_0005 
    + soft_tissue_0001 + combine_0001 + combine_0005 + combine_001,
    'Window setting': ['WL=400, WW=1800'] * 21 +
                    ['WL=50, WW=250'] * 21 +
                    ['Combined'] * 21,
        'U-Net configuration': ['1']*7 + ['2']*7 + ['3']*7 + ['4']*7 + ['5']*7 + ['6']*7 + ['7']*7 + ['8']*7 + ['9']*7,
     'Learning rate': ['0.001'] * 7 + ['0.0005'] * 7 + ['0.0001'] * 7 +
                     ['0.001'] * 7 + ['0.0005'] * 7 + ['0.0001'] * 7 +
                     ['0.001'] * 7 + ['0.0005'] * 7 + ['0.0001'] * 7               
    }

# Convert 'Weight [kg]' to numeric
df = pd.DataFrame(data)
df['Weight [kg]'] = pd.to_numeric(df['Weight [kg]'], errors='coerce')

# Sort the DataFrame by 'Weight [kg]'
df = df.sort_values(by='Weight [kg]')

# Create the violin plot
sns.violinplot(x='Weight [kg]', y='Volume discrepancy [%]', data=df, color="lightgray")

# Overlay the data points
sns.swarmplot(x='Weight [kg]', y='Volume discrepancy [%]', data=df, alpha=0.6)

# Rotate x-axis labels for better readability
#plt.xticks(rotation=45)
plt.tight_layout()

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'violin_by_weight.png')
plt.savefig(output_path, dpi=300)
plt.show()