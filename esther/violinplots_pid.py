import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

bone_0005 = [0.940, 0.935, 0.886, 0.913, 0.912, 0.946, 0.862]
bone_001 = [0.940, 0.933, 0.878, 0.913, 0.926, 0.950, 0.892]
soft_tissue_0005 = [0.924, 0.930, 0.797, 0.924, 0.949, 0.956, 0.745]
soft_tissue_001 = [0.947, 0.904, 0.858, 0.887, 0.806, 0.922, 0.929]



f1_107 = [0.940, 0.940, 0.924, 0.947]
f1_111 = [0.935, 0.933, 0.930, 0.904]  
f1_16 = [0.886, 0.878, 0.797, 0.858]
f1_3 = [0.913, 0.913, 0.924, 0.887]
f1_43 = [0.912, 0.926, 0.949, 0.806]
f1_51 = [0.946, 0.950, 0.956, 0.922]
f1_56 = [0.862, 0.892, 0.745, 0.929]



# Sample data
data = {
    'Patient-ID': ['107', '107', '107', '107',
            '111', '111', '111', '111', 
            '16', '16', '16', '16', 
            '3', '3', '3', '3', 
            '43', '43', '43', '43', 
            '51', '51', '51', '51', 
            '56', '56', '56', '56'],
    'f1-score':  f1_107 + f1_111 + f1_16 + f1_3 + f1_43 + f1_51 + f1_56,
    }

# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
sns.violinplot(x='Patient-ID', y='f1-score', data=df, color='lightgrey')

# Overlay the data points
#sns.swarmplot(x='Patient-ID', y='f1-score', data=df, alpha=0.6, dodge=True)

# Show the plot
plt.show()
plt.savefig('fig/violin_plot5.png')

