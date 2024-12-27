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

# Read data from CSV file
data = pd.read_csv("data/cell0_0.csv")
frequencies = data["freq"].values
resistance = data["resistance"].values
theta = data["theta"].values

# Convert resistance and theta to complex impedance
z_data = resistance * np.exp(1j * theta)

# Fit the model
fitted_model = fit_nyquist(frequencies, z_data, time_constants)
print("Fitted Model Parameters:", fitted_model)

# Calculate fitted impedance
z_fitted = np.array([calculate_impedance(fitted_model, w) for w in frequencies])

print("Time constants")
for i in range(1, len(fitted_model), 2):
    print(fitted_model[i]*fitted_model[i+1])

# Plot the results
plt.figure(figsize=(8, 8))
plt.plot(z_data.real, -z_data.imag, 'o', color='blue', label='Data')
plt.plot(z_fitted.real, -z_fitted.imag, 'o-', color='orange', label='Fitted')
plt.xlabel('Real(Z)')
plt.ylabel('-Imag(Z)')
plt.title('Nyquist Plot')
plt.legend()
plt.grid()
plt.show()
