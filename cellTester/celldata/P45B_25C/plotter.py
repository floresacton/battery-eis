import pandas as pd
import matplotlib.pyplot as plt
import sys

# Accept filename as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# Read the CSV file and ignore the header row
# Read the CSV file and skip the first row
data = pd.read_csv(filename, header=None, skiprows=1)

# Select two specific columns (e.g., column 1 and column 2)
x = data.iloc[:, 3]  # First column
y = data.iloc[:, 1]  # Second column

DCIR = 0.015
current = 1
y_DCIR_offset = [point+DCIR*current for point in y]

# Plot the data
plt.plot(x, y, linestyle='-', marker='', linewidth=1.0, label='1A discharge cell CCV')
plt.plot(x, y_DCIR_offset, linestyle='-', marker='', linewidth=1.0, label='DCIR compensated CCV')
plt.xlabel('Charge (mAh)', fontsize=18)
plt.ylabel('Voltage (V)', fontsize=18)
plt.title('OCV vs SOC of P45B', fontsize=18)
plt.legend()
plt.show()