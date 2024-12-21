import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

for x in range(5):
    # Read the CSV file
    data = pd.read_csv('data/cellm2_'+str(x)+'.csv')
    print(data.columns)

    # Extract resistance and theta columns
    resistance = data['resistance'].values
    theta = -data['theta'].values

    # Plot the polar data
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection='polar')
    ax.plot(theta, resistance, marker='o', markersize=3)

    # Set labels
    ax.set_title('Polar Plot of Resistance vs. Theta')
    ax.set_xlabel('Theta (radians)')
    ax.set_ylabel('Resistance')

    plt.show()
