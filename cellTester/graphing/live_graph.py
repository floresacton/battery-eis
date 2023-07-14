import matplotlib.pyplot as plt
import matplotlib.animation as animation

def create_live_graph(window_size):
    # Function to update the data for the live graph
    def update_data(i):
        line.set_ydata(y_data)  # Update the y-data for the line

    # Initialize the figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(0, window_size - 1)
    ax.set_ylim(0, 100)
    line, = ax.plot([], [], lw=2)

    # Data container to hold the y-data for the graph
    y_data = [0] * window_size

    # Create the animation
    ani = animation.FuncAnimation(fig, update_data, interval=200)  # Interval is in milliseconds

    # Display the live updating graph
    plt.title('Live Updating Graph with Changing Window')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.grid(True)

    # Return the figure and animation objects in case you want to use them later
    return fig, ani, y_data
