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
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 4))
    heatmap = plt.pcolor(array)
    fig.colorbar(heatmap)
    plt.tight_layout()


def plot_colorbar(array):
    """
    画热力图
    :param array:横轴帧数，纵轴数值
    :return:
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 4))
    heatmap = plt.pcolor(array)
    fig.colorbar(heatmap)
    plt.tight_layout()
    plt.show()
