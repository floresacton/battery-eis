import matplotlib.pyplot as plt


def plot(pts1, pts2):
    # Separate the list of tuples
    x1, y1 = zip(*pts1)
    x2, y2 = zip(*pts2)

    # Plot each group with different styles
    plt.plot(x1, y1, color='blue', label='Chan1', marker='o', linestyle='-', linewidth=2)
    plt.plot(x2, y2, color='red', label='Chan2', marker='x', linestyle='--', linewidth=2)

    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.title('Scope')

    plt.legend()

    plt.show()