import numpy as np


# y = A*cos(wt + C) + D
def sine_fit(points, freq):
    ts = points[:, 0]
    ys = points[:, 1]

    ts = 2 * np.pi * freq * ts
    matrix = np.column_stack((np.sin(ts), np.cos(ts), np.ones_like(ts)))

    beta, _, _, _ = np.linalg.lstsq(matrix, ys, rcond=None)
    a, b, offset = beta

    amp = np.sqrt(a**2 + b**2)
    phi = np.arctan2(b, a)

    return amp, phi, offset
