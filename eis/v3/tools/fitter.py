import numpy as np


# y = A*cos(wt + C) + D
def sine_fit(points, freq):
    ts = points[:, 0].astype(np.float64)
    ys = points[:, 1].astype(np.float64)

    ts = 2 * np.pi * freq * ts
    matrix = np.column_stack((np.sin(ts), np.cos(ts), np.ones_like(ts)))

    beta, _, _, _ = np.linalg.lstsq(matrix, ys, rcond=None)
    a, b, offset = beta

    amp = np.sqrt(a**2 + b**2)
    phi = np.arctan2(b, a)

    return amp, phi, offset

# def sine_fit(points, freq):
#     ts = points[:, 0].astype(np.float64)  # Use higher precision float
#     ys = points[:, 1].astype(np.float64)  # Use higher precision float

#     # Scale time to avoid precision issues if necessary
#     scale_factor = 1000  # Example scale factor
#     ts_scaled = ts * scale_factor  # Scale time values

#     # Convert time to angular frequency
#     angular_freq = 2 * np.pi * freq * ts * scale_factor

#     # Create the design matrix for sine and cosine terms
#     matrix = np.column_stack((np.sin(angular_freq),
#                                np.cos(angular_freq),
#                                np.ones_like(angular_freq)))

#     # Perform least squares fitting
#     beta, _, _, _ = np.linalg.lstsq(matrix, ys, rcond=None)
#     a, b, offset = beta

#     # Calculate amplitude and phase
#     amp = np.sqrt(a**2 + b**2)
#     phi = np.arctan2(b, a)

#     return amp, phi, offset