import scikits.talkbox as tb
from scikits.talkbox.linpred import levinson_lpc
import numpy as np


def lpc_to_cc(lpc, n_lpc, n_lpcc):
    lpcc = np.zeros(n_lpcc)
    lpcc[0] = lpc[0]
    for n in range(1, n_lpc):
        lpcc[n] = lpc[n]
        for l in range(0, n):
            lpcc[n] += lpc[l] * lpcc[n - l - 1] * (n - l) / (n + 1)
    for n in range(n_lpc, n_lpcc):
        lpcc[n] = 0
        for l in range(0, n_lpc):
            lpcc[n] += lpc[l] * lpcc[n - l] * (n - l) / n
    return -lpcc[1:]


def lpcc(frames, n_lpc, n_lpcc):
    """
    n_lpc:lpc阶数
    n_lpcc:lpcc阶数
    """
    lpcs = []
    lpccs = []
    for frame in frames:
        lpc = levinson_lpc.lpc(frame, n_lpc)[0]
        lpcc = lpc_to_cc(lpc, n_lpc, n_lpcc)
        lpcs.append(lpc)
        lpccs.append(lpcc)
    return lpcs, lpccs
