import numpy as np
import matplotlib.pyplot as plt


def plot_array(array):
    x_ = np.arange(0, len(array))
    plt.plot(x_, array)
    plt.show()


def scatter_array(array):
    x_ = np.arange(0, len(array))
    plt.scatter(x_, array)
    plt.show()


def plot_colormesh(array):
    shape = np.shape(array)
    plt.pcolormesh(range(shape[1]), range(shape[0]), array)
