import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import get_cmap

# Create the figure
plt.figure(figsize=(10, 8))

# Define a colormap with distinct colors for each cell
colormap = get_cmap('tab20')  # Use a qualitative colormap for distinct colors

# Plot data for each cell and its tests
for i in range(5):  # Loop over cells
    color = colormap(i / 5.0)  # Assign a distinct color to each cell
    for j in range(5):  # Loop over tests
        # Read the CSV file
        data = pd.read_csv(f'data/cell{i}_{j}.csv')
        
        # Extract resistance and theta columns
        resistance = data['resistance'].values
        theta = -data['theta'].values
        
        # Convert to real (a) and imaginary (b) parts
        a = resistance * np.cos(theta)
        b = resistance * np.sin(theta)

        # Plot the data without adding individual test labels
        plt.plot(a, b, marker='o', markersize=3, color=color, alpha=0.8)
    
    # Add a single legend entry for the cell
    plt.plot([], [], marker='o', markersize=5, color=color, label=f'Cell {i}')

# Set axis labels and title with increased font sizes
plt.title('Nyquist Plot, 0.1Hz to 300Hz', fontsize=20)  # Increased font size
plt.xlabel('Re(Z), (Ohms)', fontsize=16, labelpad=10)  # Add extra padding to label
plt.ylabel('Im(Z), (Ohms)', fontsize=16, labelpad=10)  # Add extra padding to label

# Adjust the tick label sizes
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add a legend for cells with increased font size
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize=14, title="Cells", title_fontsize=16)

plt.axis('equal')  # Ensure equal scaling for x and y axes

# Show grid and tighten layout
plt.grid(True)
plt.tight_layout()
plt.show()
