import numpy as np
from pyhht import EMD
from scipy.signal import hilbert


def pre_emphasis(sound_array, u):
    """
    u:预加重系数  coefficient
    """
    return np.append(sound_array[0], sound_array[1:] - u * sound_array[:-1])


# 分帧、加窗
def enframe(signal, nw, inc, window_func=None):
    """
    signal:原始信号
    nw:帧长
    inc:相邻帧间隔,步长
    window_func:窗函数
    """
    signal_length = len(signal)
    if signal_length < nw:
        # nf为帧的数量
        nf = 1
    else:
        # np.ceil 计算大于该值的最小整数
        nf = int(np.ceil((1.0 * signal_length - nw + inc) / inc))
    pad_length = int((nf - 1) * inc + nw)  # 所有帧的帧长之和
    zeros = np.zeros((pad_length - signal_length,))  # 补0
    pad_signal = np.concatenate((signal, zeros))
    indices = np.tile(np.arange(0, nw), (nf, 1)) + np.tile(np.arange(0, nf * inc, inc), (nw, 1)).T
    indices = np.array(indices, dtype=np.int32)
    frames = pad_signal[indices]
    if window_func is not None:
        win = np.tile(window_func, (nf, 1))
        return frames * win
    return frames


def hht(signal):
    decomposer = EMD(signal)
    imfs = decomposer.decompose()
    ht = hilbert(imfs)
    return imfs, ht
