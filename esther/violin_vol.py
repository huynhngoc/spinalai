"""
Plotting violin plots for volume deviations for different windowing and learning rates
"""

# Importing libraries
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

# data
bone_001 = [2.48, -7.75, 0.35, -0.09, 10.87, 5.42, -4.94]
bone_0005 = [-3.45, -9.96, -9.59, -5.17, 12.23, 3.96, -4.24]
bone_0001 = [-0.351, -3.031, -1.937, -3.279, 0.944, 2.815, -4.097]
soft_tissue_001 = [-5.34, -25.78, -1.93, -11.67, -1.10, -10.93, -7.81]
soft_tissue_0005 = [0.83, -50.03, 4.47, 2.13, 33.56, -8.89, -10.49]
soft_tissue_0001 = [-10.302, -20.526, 3.376, 2.230, 3.158, -8.430, -25.707]
combine_0001 = [5.341, -14.989, 2.180, 0.532, 44.829, -2.059, -7.891]
combine_0005 = [-1.048, -17.757, -1.330, 0.639, 24.799, 1.630, -12.894]
combine_001 = [5.879, -24.663, 4.585, 5.5604, 3.3114, -4.418, -2.757]

print('mean for each windowing')
print(np.mean(np.abs(bone_0001 + bone_0005 + bone_001)))
print(np.mean(np.abs(combine_001 + combine_0005 + combine_0001)))
print(np.mean(np.abs(soft_tissue_0001 + soft_tissue_0005 + soft_tissue_001)))

print('median for each windowing')
print(np.median((bone_0001 + bone_0005 + bone_001)))
print(np.median((combine_001 + combine_0005 + combine_0001)))
print(np.median((soft_tissue_0001 + soft_tissue_0005 + soft_tissue_001)))

print('std for each windowing')
print(np.std((bone_0001 + bone_0005 + bone_001)))
print(np.std((combine_001 + combine_0005 + combine_0001)))
print(np.std((soft_tissue_0001 + soft_tissue_0005 + soft_tissue_001)))

print('median for each learning rate')
print(np.median((bone_0001 + soft_tissue_0001 + combine_0001)))
print(np.median((bone_0005 + soft_tissue_0005 + combine_0005)))
print(np.median((bone_001 + soft_tissue_001 + combine_001)))

print('std for each learning rate')
print(np.std((bone_0001 + soft_tissue_0001 + combine_0001)))
print(np.std((bone_0005 + soft_tissue_0005 + combine_0005)))
print(np.std((bone_001 + soft_tissue_001 + combine_001)))



# Sample data
data = {
    'Sample-ID': ['3', '16', '43', '51', '56', '107', '111']* 9,
    'Volume discrepancy [%]':  soft_tissue_0001 + soft_tissue_0005 +soft_tissue_001 + 
    bone_0001 + bone_0005 + bone_001 + combine_0001 + combine_0005 + combine_001,
    'Window setting': ['WL=50, WW=250'] * 21 +
                    ['WL=400, WW=1800'] * 21 +
                    ['Combined'] * 21,
        'U-Net configuration': ['1']*7 + ['2']*7 + ['3']*7 + ['4']*7 + ['5']*7 + ['6']*7 + ['7']*7 + ['8']*7 + ['9']*7,
     'Learning rate': ['0.0001'] * 7 + ['0.0005'] * 7 + ['0.001'] * 7 +
                     ['0.0001'] * 7 + ['0.0005'] * 7 + ['0.001'] * 7 +
                     ['0.0001'] * 7 + ['0.0005'] * 7 + ['0.001'] * 7               
    }

# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
ax = sns.violinplot(x='Window setting', y='Volume discrepancy [%]', data=df, color="lightgray", cut=0)
ax = plt.gca() # get current axis
ax.set_ylim(-60, 60)

# Overlay the data points   
sns.swarmplot(x='Window setting', y='Volume discrepancy [%]', data=df, alpha=0.6, hue='Learning rate')
plt.legend(title="Learning rate", loc='upper center')
plt.hlines(y=0, xmin=-0.5, xmax=2.5, color='black', linestyle='--', linewidth=1)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'win_vol.png')
plt.savefig(output_path, dpi=300)
plt.show()



# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
ax = sns.violinplot(x='Learning rate', y='Volume discrepancy [%]', data=df, color="lightgray", cut=0)
ax = plt.gca()  # Get current axis
ax.set_ylim(-60, 60)

# Overlay the data points   
sns.swarmplot(x='Learning rate', y='Volume discrepancy [%]', data=df, alpha=0.6, hue='Window setting')
plt.legend(title="Window setting", loc='upper right')

# Rotate x-axis labels
#plt.xticks(rotation=45)
plt.hlines(y=0, xmin=-0.5, xmax=2.5, color='black', linestyle='--', linewidth=1)

# Adjust layout to prevent labels from being cut off
plt.tight_layout()

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'lr_vol.png')
plt.savefig(output_path, dpi=300)
plt.show()



# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
ax = sns.violinplot(x='U-Net configuration', y='Volume discrepancy [%]', data=df, color="lightgray", cut=0)
ax = plt.gca()  # Get current axis
ax.set_ylim(-60, 60)

# Overlay the data points   
sns.swarmplot(x='U-Net configuration', y='Volume discrepancy [%]', data=df, alpha=0.6, hue='Learning rate')
plt.legend(title="Window setting", loc='upper right')


# Adjust layout to prevent labels from being cut off
plt.tight_layout()
plt.hlines(y=0, xmin=-0.5, xmax=8.5, color='black', linestyle='--', linewidth=1)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'config_vol.png')
plt.savefig(output_path, dpi=300)
plt.show()




# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
ax = sns.violinplot(x='Sample-ID', y='Volume discrepancy [%]', data=df, color="lightgray", cut=0)
ax = plt.gca()  # Get current axis
ax.set_ylim(-60, 60)

# Overlay the data points   
sns.swarmplot(x='Sample-ID', y='Volume discrepancy [%]', data=df, alpha=0.6, hue='Window setting')
plt.legend(title="Window setting", loc='upper right')

# Rotate x-axis labels
#plt.xticks(rotation=45)

# Adjust layout to prevent labels from being cut off
plt.tight_layout()
plt.hlines(y=0, xmin=-0.5, xmax=6.5, color='black', linestyle='--', linewidth=1)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'pid_vol.png')
plt.savefig(output_path, dpi=300)
plt.show()