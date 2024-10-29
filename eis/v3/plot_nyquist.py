import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Read the CSV file
data = pd.read_csv('data/nyquist.csv')
print(data.columns)

# Extract resistance and theta columns
resistance = data['resistance']
theta = data['theta']

# Plot the polar data
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, projection='polar')
ax.plot(theta, resistance, marker='o', markersize=3)

# Set labels
ax.set_title('Polar Plot of Resistance vs. Theta')
ax.set_xlabel('Theta (radians)')
ax.set_ylabel('Resistance')

plt.show()