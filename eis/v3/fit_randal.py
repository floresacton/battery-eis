import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

rbound = (1e-6, 1e-1)
cbound = (1e-2, 1e5)
time_constants = 4

def calculate_impedance(model, frequency):
    z = model[0]
    for i in range(1, len(model), 2):
        if (model[i] != 0):
            z += 1 / (1 / model[i] + 1j * frequency * 2 * math.pi * model[i+1])
    return z

def objective_function(params, frequencies, z_data):
    z_model = np.array([calculate_impedance(params, w) for w in frequencies])
    error = np.abs(z_model - z_data)  # Directly minimize magnitude difference
    return np.sum(error)

def fit_nyquist(frequencies, z_data, time_constants):
    bounds = [rbound]
    for i in range(time_constants):
        bounds.append(rbound)
        bounds.append(cbound)

    result = differential_evolution(
        objective_function, 
        bounds,
        args=(frequencies, z_data),
        strategy='best1bin',
        maxiter=5000,
        tol=1e-5
    )
    if result.success:
        return result.x
    else:
        raise ValueError("Optimization failed: " + result.message)

# data = pd.read_csv("data/cell0_1.csv")
# frequencies = data["freq"].values
# resistance = data["resistance"].values
# theta = data["theta"].values

# Read data from CSV files
frequencies = np.array([])
resistance = np.array([])
theta = np.array([])

test_frequencies = np.array([])

for i in range(5):  # Loop over cells
    for j in range(5):  # Loop over tests
        # Read the CSV file
        data = pd.read_csv(f'data/cell{i}_{j}.csv')

        test_frequencies = data["freq"].values

        frequencies = np.concatenate((frequencies, data["freq"].values))
        resistance = np.concatenate((resistance, data["resistance"].values))
        theta = np.concatenate((theta, data["theta"].values))

# Convert resistance and theta to complex impedance
z_data = resistance * np.exp(1j * theta)

# Fit the model
fitted_model = fit_nyquist(frequencies, z_data, time_constants)
# print("Fitted Model Parameters:", fitted_model)
print("Fitted Model Parameters:")
print("R =", fitted_model[0])
for i in range(time_constants):
    print(f"R{i+1} =", fitted_model[1 + 2*i])
    print(f"C{i+1} =", fitted_model[1 + 2*i+1])

# Calculate fitted impedance
z_fitted = np.array([calculate_impedance(fitted_model, w) for w in test_frequencies])

print("Time constants:")
for i in range(1, len(fitted_model), 2):
    print(f"T{i//2+1} =", fitted_model[i]*fitted_model[i+1])

Rtot = fitted_model[0]
for i in range(time_constants):
    Rtot += fitted_model[1 + 2*i]
print("DC resistance =", Rtot)

# Plot the results
plt.figure(figsize=(10, 8))

plt.axis('equal')  # Ensure equal scaling for x and y axes

plt.plot(z_data.real, -z_data.imag, 'o', color='blue', label='EIS Data')
plt.plot(z_fitted.real, -z_fitted.imag, 'o-', color='orange', label='Fitted Model')
plt.xlabel('Re(Z), (Ohms)', fontsize=16, labelpad=0)
plt.ylabel('Im(Z), (Ohms)', fontsize=16, labelpad=10)
schr = ('s' if time_constants > 1 else '')
plt.title(f'Nyquist Plot, ERM with {time_constants} RC circuit{schr}', fontsize=20)
plt.legend(fontsize=14, title_fontsize=16)
plt.grid()
plt.show()
