import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the CSV file into a Pandas DataFrame
data = pd.read_csv('output.csv')

# Extract the columns of data
x = np.array(data['T'])
y1 = np.array(data['V'])
y2 = np.array(data['I'])

# Plot the data using Matplotlib
fig, ax1 = plt.subplots()

# Plot the first line with its own y-axis
ax1.plot(x, y1, label='V')
ax1.set_xlabel('X-axis')
ax1.set_ylabel('Voltage', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Create a second y-axis and plot the second line
ax2 = ax1.twinx()
ax2.plot(x, y2, color='tab:red', label='Column 3')
ax2.set_ylabel('Current', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Set title and display legend
plt.title('Data Plot')
plt.legend(loc='upper left')

# Display the plot
plt.show()
