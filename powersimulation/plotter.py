import matplotlib.pyplot as plt
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Plot power vs. time from a data file.')
parser.add_argument('file', type=str, help='Path to the input data file')
args = parser.parse_args()

# File path from command-line argument
file_path = args.file

# Initialize lists to store the data
time = []
power = []

# Read the file and extract data
try:
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                t, p = map(float, line.split())  # Split and convert to float
                time.append(t)
                power.append(p)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit(1)

# Plot the data
plt.figure(figsize=(8, 6))
plt.plot(time, power, marker='o', markersize=1, linestyle='-', linewidth=2, color='b', label='Power (W)')
plt.title('Spin Jump', fontsize=16)  # Increased title font size
plt.xlabel('Time (seconds)', fontsize=14)  # Increased x-axis label font size
plt.ylabel('Power (watts)', fontsize=14)  # Increased y-axis label font size
plt.grid(True)
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
