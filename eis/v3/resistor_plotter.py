import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import get_cmap

# Create the figure
plt.figure(figsize=(10, 8))

filenames = ['data/resistor_0.csv', 'data/shunt_0.csv']
nicknames = ['Fake Cell', '10mΩ Shunt Resistor']

for i in range(len(filenames)):

    # Read the CSV file
    data = pd.read_csv(filenames[i])
    
    # Extract resistance and theta columns
    resistance = data['resistance'].values
    theta = -data['theta'].values
    
    # Convert to real (a) and imaginary (b) parts
    a = resistance * np.cos(theta)
    b = resistance * np.sin(theta)

    # Plot the data without adding individual test labels
    plt.plot(a, b, marker='o', markersize=3, alpha=0.8, label=nicknames[i])


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
