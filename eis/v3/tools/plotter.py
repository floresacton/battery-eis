import matplotlib.pyplot as plt

colors = [
    "b",  # blue
    "g",  # green
    "r",  # red
    "c",  # cyan
    "m",  # magenta
    "y",  # yellow
    "k",  # black
    "w",  # white
]


def plot(datasets):
    i = 0
    for dataset in datasets:
        x, y = zip(*dataset)
        plt.scatter(x, y, color=colors[i], label=str(i), s=2)
        i+=1

    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Voltage')
    plt.title('Scope')

    plt.legend()

    plt.show()