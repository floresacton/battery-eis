from live_graph import create_live_graph
import matplotlib.pyplot as plt
import random

def generate_random_data():
    return random.randint(0, 100)

if __name__ == "__main__":
    window_size = 50
    fig, ani, y_data = create_live_graph(window_size)

    while True:
        new_data_point = generate_random_data()
        y_data.append(new_data_point)  # Append new data point
        if len(y_data) > window_size:
            y_data.pop(0)  # Remove the oldest data point to maintain the window size
        plt.pause(0.2)  # Pause to update the graph

