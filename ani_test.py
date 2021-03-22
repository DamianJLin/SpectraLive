import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import time


def timer():
    global start_time
    return time.time() - start_time


def rand_sin(err=0.2):
    """
    Return a random value equal to sin(x) in expectation value.
    :param err:
    :return:
    """
    global start_time

    while True:
        x = timer()

        yield np.sin(np.pi * x) + err * 2 * (0.5 - np.random.rand())


class Animator:
    def __init__(self, ax_, t_window=6):
        self.ax = ax_
        self.t_window = t_window  # Time interval displayed.
        self.dt = 0.1
        self.interval = int((1/self.dt) * 1000)  # Time interval needed between frames
        self.ax.set_xlim(0, -t_window)
        self.ax.set_ylim(-1.5, 1.5)

        self.t_data_size = int(self.t_window / self.dt) + 1  # Number of points with spacing dt self.t_window corresponds to.

        self.t_data = np.linspace(0, -t_window, self.t_data_size, endpoint=True)
        self.y_data = [0] * self.t_data_size

        self.line = Line2D(self.t_data, self.y_data)

        self.ax.add_line(self.line)
        self.ax.grid('minor')

    def update(self, y):

        # Shift y_data.
        self.y_data.pop(-1)
        self.y_data.insert(0, y)
        self.line.set_data(self.t_data, self.y_data)
        self.ax.set_title(f't={np.round(timer(), 1)}')

        return self.line,


if __name__ == '__main__':
    start_time = time.time()

    fig, ax = plt.subplots()
    animator = Animator(ax)

    ani = anim.FuncAnimation(fig, animator.update, rand_sin, interval=100, blit=False)
    plt.show()
