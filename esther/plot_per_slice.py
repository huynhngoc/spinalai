import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

pid = 3

# Load the data
df = pd.read_csv(f'data//3_f021_bone_0001.csv', sep=',')

#df = pd.DataFrame(df[df['patient_idx']==pid])
#df.set_index('slice_idx', inplace=True)
print(df.head())
#df['slice_idx']

df2 = pd.read_csv(f'outputs//volume_{pid}.csv', sep=';')
df2 = pd.DataFrame(df2)
print(df2.head())

# Plot the data
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot F1 Score on the primary y-axis
sns.lineplot(x='slice_idx', y='f1_score', data=df, marker='o', ax=ax1, label='F1 Score')
#sns.lineplot(x='slice_idx', y='precision', data=df, marker='o', ax=ax1, label='precision')
#sns.lineplot(x='slice_idx', y='recall', data=df, marker='o', ax=ax1, label='recall')
ax1.set_xlabel('Slice')
ax1.set_ylabel('F1 Score', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid()

# Create a secondary y-axis for Volume
ax2 = ax1.twinx()
sns.lineplot(x='slice_idx', y='volume', data=df2, marker='o', ax=ax2, color='orange', label='Volume')
ax2.set_ylabel('Volume [$cm^3$]', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Add a title and show the plot
plt.title('F1 Score and Volume by Slice')
fig.tight_layout()

# Save the figure in the 'figures' folder
output_folder = 'figures'
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
output_path = os.path.join(output_folder, f'plot_per_slice_pid_{pid}.png')
plt.savefig(output_path, dpi=300)
plt.show()
