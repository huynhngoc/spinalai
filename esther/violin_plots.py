# Library imports
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os

# define the data for the violin plots
wide_001 = [0.921, 0.934, 0.855, 0.917, 0.902, 0.908]
wide_0005 = [0.919, 0.924, 0.873, 0.932, 0.892, 0.928]
wide_0001 = [0.910, 0.917, 0.896, 0.935, 0.913, 0.921]

narrow_001 = [0.938, 0.874, 0.879, 0.862, 0.893, 0.88]
narrow_0005 = [0.912, 0.932, 0.855, 0.945, 0.876, 0.925]
narrow_0001 = [0.915, 0.960, 0.805, 0.922, 0.890, 0.941]

combine_0001 = [0.936, 0.951, 0.887, 0.955, 0.921, 0.938]
combine_0005 = [0.932, 0.920, 0.850, 0.949, 0.911, 0.943]
combine_001 = [0.910, 0.920, 0.890, 0.940, 0.930, 0.950]  

prec_wide_001 = [0.942, 0.932, 0.861, 0.936, 0.882, 0.915]
prec_wide_0005 = [0.927, 0.893, 0.904, 0.955, 0.922, 0.942]
prec_wide_0001 = [0.912, 0.874, 0.860, 0.976, 0.906, 0.919]
prec_narrow_001 = [0.952,0.845, 0.883, 0.876, 0.929, 0.928]
prec_narrow_0005 = [0.947, 0.967,0.929, 0.951,0.900, 0.941]
prec_narrow_0001 = [0.918, 0.962, 0.942, 0.948, 0.951, 0.940]
prec_combine_0001 = [0.925, 0.967, 0.939, 0.938, 0.912, 0.944]
prec_combine_0005 = [0.958, 0.908, 0.944, 0.949, 0.942, 0.937]
prec_combine_001 = [0.924, 0.959, 0.778, 0.945, 0.915, 0.923]

rec_wide_001 = [0.902, 0.935, 0.866, 0.899, 0.924, 0.903]
rec_wide_0005 = [0.912, 0.957, 0.851, 0.910, 0.866, 0.915]
rec_wide_0001 = [0.909, 0.963, 0.937, 0.898, 0.921, 0.924]
rec_narrow_001 = [0.925, 0.906, 0.875, 0.848, 0.864, 0.836]
rec_narrow_0005 = [0.882, 0.898, 0.802, 0.938, 0.855, 0.913]
rec_narrow_0001 = [0.917, 0.958, 0.706, 0.897, 0.837, 0.944]
rec_combine_0001 = [0.950, 0.937, 0.849, 0.972, 0.931, 0.936]
rec_combine_0005 = [0.910, 0.933, 0.788, 0.949, 0.885, 0.950]
rec_combine_001 = [0.929, 0.952, 0.910, 0.954, 0.897, 0.960]






# Sample data
data = {
    'Window setting': ['WL=50, WW=250'] * 18 +
                    ['WL=400, WW=1800'] * 18 +
                    ['Combined'] * 18,
    'Dice-score': narrow_0001 + narrow_0005 + narrow_001 +
                wide_0001 + wide_0005 + wide_001 +
                combine_0001 + combine_0005 + combine_001,
    'Precision': prec_narrow_0001 + prec_narrow_0005 + prec_narrow_001 +
                prec_wide_0001 + prec_wide_0005 + prec_wide_001 +
                prec_combine_0001 + prec_combine_0005 + prec_combine_001,
    'Recall': rec_narrow_0001 + rec_narrow_0005 + rec_narrow_001 +
                rec_wide_0001 + rec_wide_0005 + rec_wide_001 +
                rec_combine_0001 + rec_combine_0005 + rec_combine_001,
    'Learning rate': ['0.0001'] * 6 + ['0.0005'] * 6 + ['0.001'] * 6 +
                     ['0.0001'] * 6 + ['0.0005'] * 6 + ['0.001'] * 6 +
                     ['0.0001'] * 6 + ['0.0005'] * 6 + ['0.001'] * 6,
    'U-Net configuration' : ['1']*6 + ['2']*6 + ['3']*6 + 
                            ['4']*6 + ['5']*6 + ['6']*6 +
                            ['7']*6 + ['8']*6 + ['9']*6
}


"""
Violin plot for Dice score for each config
"""
# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot for Window Width
sns.violinplot(x='U-Net configuration', y='Dice-score', data=df, color="lightgray", cut=0)

# Swarm plot
sns.swarmplot(x='U-Net configuration', y='Dice-score', data=df, hue='Learning rate', alpha=0.6)

ax = plt.gca() # get current axis
ax.set_ylim(0.75, 1.0)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'config_dice.png')
plt.savefig(output_path, dpi=300)
plt.show()

"""
Violin plot for Dice score for each Window setting
"""
# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot for Window Width
sns.violinplot(x='Window setting', y='Dice-score', data=df, color="lightgray", cut=0)

# Swarm plot
sns.swarmplot(x='Window setting', y='Dice-score', data=df, hue='Learning rate', alpha=0.6)

ax = plt.gca() # get current axis
ax.set_ylim(0.75, 1.0)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'dist_fold_win.png')
plt.savefig(output_path, dpi=300)
plt.show()

"""
Violin plots for Dice score for each learning rate"""
# Create the violin plot for Window Width
sns.violinplot(x='Learning rate', y='Dice-score', data=df, color="lightgray", cut=0)

# Swarm plot
sns.swarmplot(x='Learning rate', y='Dice-score', data=df, hue='Window setting', alpha=0.6)

ax = plt.gca() # get current axis
ax.set_ylim(0.75, 1.0)

# Save the figure
output_path = os.path.join(output_folder, 'dist_fold_lr.png')
plt.savefig(output_path, dpi=300)
plt.show()

"""
Violin plots for Recall for each window setting
"""
# Create the violin plot for Window Width
sns.violinplot(x='Window setting', y='Recall', data=df, color="lightgray", cut=0)

# Swarm plot
sns.swarmplot(x='Window setting', y='Recall', data=df, hue='Learning rate', alpha=0.6)

ax = plt.gca() # get current axis
ax.set_ylim(0.75, 1.0)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'dist_rec_win.png')
plt.savefig(output_path, dpi=300)
plt.show()

"""
Violin plots of recall for each Learning rate
"""
# Create the violin plot for Window Width
sns.violinplot(x='Learning rate', y='Recall', data=df, color="lightgray", cut=0)

# Swarm plot
sns.swarmplot(x='Learning rate', y='Recall', data=df, hue='Window setting', alpha=0.6)

ax = plt.gca() # get current axis
ax.set_ylim(0.75, 1.0)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'dist_rec_lr.png')
plt.savefig(output_path, dpi=300)
plt.show()

"""
Violin plots for Precision for each window setting
"""

# Create the violin plot for Window Width
sns.violinplot(x='Window setting', y='Precision', data=df, color="lightgray", cut=0)

# Swarm plot
sns.swarmplot(x='Window setting', y='Precision', data=df, hue='Learning rate', alpha=0.6)

ax = plt.gca() # get current axis
ax.set_ylim(0.75, 1.0)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'dist_prec_win.png')
plt.savefig(output_path, dpi=300)
plt.show()

"""
Violin plots for precision for each learning rate
"""

# Create the violin plot for Window Width
sns.violinplot(x='Learning rate', y='Precision', data=df, color="lightgray", cut=0)

# Swarm plot
sns.swarmplot(x='Learning rate', y='Precision', data=df, hue='Window setting', alpha=0.6)

ax = plt.gca() # get current axis
ax.set_ylim(0.75, 1.0)

# Save the figure
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, 'dist_prec_lr.png')
plt.savefig(output_path, dpi=300)
plt.show()