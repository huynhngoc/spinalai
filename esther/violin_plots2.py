import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

wide_001 = [0.940, 0.933, 0.878, 0.913, 0.926, 0.950, 0.892]
wide_0005 = [0.940, 0.935, 0.886, 0.913, 0.912, 0.946, 0.862]
narrow_001 = [0.947, 0.904, 0.858, 0.887, 0.806, 0.922, 0.929]
narrow_0005 = [0.924, 0.930, 0.797, 0.924, 0.949, 0.956, 0.745]

print(wide_001+narrow_001)

# Sample data
data = {
    'Window_width': ['soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 
                     'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 
                 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)', 
                 'soft_tissue (WC=50, WW=250)', 'soft_tissue (WC=50, WW=250)',
                 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)', 
                 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)',
                 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)',
                 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)', 'bone (WC=400, WW=1800)'],
    'f1_score':  narrow_0005 + narrow_001 + wide_0005 + wide_001,
    'Learning_rate': ['0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005',
                      '0.001', '0.001', '0.001', '0.001', '0.001', '0.001', '0.001', 
                      '0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005', '0.0005',
                      '0.001', '0.001', '0.001', '0.001', '0.001', '0.001', '0.001']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
sns.violinplot(x='Window_width', y='f1_score', data=df, color='lightgrey')

# Overlay the data points
sns.swarmplot(x='Window_width', y='f1_score', data=df, hue='Learning_rate', alpha=0.6, dodge=True)

# Show the plot
plt.show()
plt.savefig('figures/violin_plot3.png')


# Create a DataFrame
df = pd.DataFrame(data)

# Create the violin plot
sns.violinplot(x='Learning_rate', y='f1_score', data=df, color='lightgrey')

# Overlay the data points
sns.swarmplot(x='Learning_rate', y='f1_score', data=df, hue='Window_width', alpha=0.6, dodge=True)


# Show the plot
plt.show()
plt.savefig('figures/violin_plot4.png')