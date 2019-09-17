import numpy as np


# 短时能量
def cal_energy(frames):
    energy = []
    for frame in frames:
        sum = 0
        for i in frame:
            sum += i ** 2
        energy.append(sum)
    return energy


# 短时平均幅度
def cal_amplitude(frames):
    energy = []
    for frame in frames:
        sum = 0
        for i in frame:
            sum += abs(i)
        energy.append(sum)
    return energy


# 短时过零率
def cal_crossing_zero_rate(frames):
    def sgn(data):
        if data >= 0:
            return 1
        else:
            return -1

    zero_cross = []
    for frame in frames:
        sum = 0
        for i in range(len(frame)):
            sum += abs(sgn(frame[i]) - sgn(frame[i - 1]))
        sum = 0.5 * sum
        zero_cross.append(sum)
    return zero_cross


# 短时自相关函数
def self_correlation(frames, K=0):
    self_corr = []
    if K == 0:
        # K默认是帧长
        K = len(frames[0])
    for frame in frames:
        Rm = np.zeros((K, 1))
        for k in range(1, K):
            for i in range(len(frame) - k):
                Rm[k] += frame[i] * frame[i + k]
        self_corr.append(Rm)
    return self_corr


# 短时自相关函数获取f0
def get_f0_by_corr(self_corr):
    f_s = []
    for frame in self_corr:
        f_s.append(np.argmax(frame))
    return f_s


# 短时平均幅度差函数
def average_amplitude(frames, K=0):
    self_corr = []
    if K == 0:
        # K默认是帧长
        K = len(frames[0])
    for frame in frames:
        Rm = np.zeros((K, 1))
        for k in range(1, K):
            for i in range(len(frame) - k):
                Rm[k] += abs(frame[i] - frame[i + k])
        self_corr.append(Rm)
    return self_corr


# 短时平均幅度差获取f0
def get_f0_amplitude(self_corr):
    f_s = []
    for frame in self_corr:
        f_s.append(np.argmin(frame))
    return f_s
