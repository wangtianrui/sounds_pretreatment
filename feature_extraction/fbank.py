import numpy as np


def _hz2mel(hz):
    """Convert frequency to Mel frequency.
    Arguments:
        hz: Frequency.
    Returns:
        Mel frequency.
    """
    return 2595 * np.log10(1 + hz / 700.0)


def _mel2hz(mel):
    """Convert Mel frequency to frequency.
    Arguments:
        mel:Mel frequency
    Returns:
        Frequency.
    """
    return 700 * (10 ** (mel / 2595.0) - 1)


def _spectrum_magnitude(frames, NFFT):
    '''Apply FFT and Calculate magnitude of the spectrum.
    Arguments:
        frames: 2-D frames array calculated by audio2frame(...).
        NFFT:FFT size.
    Returns:
        Return magnitude of the spectrum after FFT, with shape (frames_num, NFFT).
    '''
    complex_spectrum = np.fft.rfft(frames, NFFT)
#     print(np.shape(complex_spectrum))
#     print(np.absolute(complex_spectrum)[:5])
    # 计算的是 矢量的长度
    # 为啥是 NFFT / 2  ， 因为对称性
    return np.absolute(complex_spectrum)


def _spectrum_power(frames, NFFT):
    """Calculate power spectrum for every frame after FFT.
    Arguments:
        frames: 2-D frames array calculated by audio2frame(...).
        NFFT:FFT size
    Returns:
        Power spectrum: PS = magnitude^2/NFFT
    """
    # 首先 功率谱是 傅里叶系数的平方，除以N是因为分窗把原周期扩大了N倍
    return 1.0 / NFFT * np.square(_spectrum_magnitude(frames, NFFT))


def _get_filter_banks(filters_num=20, NFFT=512, sample_rate=16000, low_freq=0, high_freq=None):
    '''Calculate Mel filter banks.
    Arguments:
        filters_num: Numbers of Mel filters.
        NFFT:FFT size. Defaulted to 512.
        sample_rate: Sampling rate. Defaulted to 16KHz.
        low_freq: Lowest frequency.
        high_freq: Highest frequency.
    '''
    # Convert frequency to Mel frequency.
    low_mel = _hz2mel(low_freq)
    high_mel = _hz2mel(high_freq)
    # Insert filters_num of points between low_mel and high_mel. In total there are filters_num+2 points
    mel_points = np.linspace(low_mel, high_mel, filters_num + 2)
    # Convert Mel frequency to frequency and find corresponding position.
    hz_points = _mel2hz(mel_points)
    # Find corresponding position of these hz_points in fft.
    bin = np.floor((NFFT + 1) * hz_points / sample_rate)
    # Build Mel filters' expression.First and third points of each filter are zeros.
    fbank = np.zeros([filters_num, int(NFFT / 2 + 1)])
    for j in range(0, filters_num):
        for i in range(int(bin[j]), int(bin[j + 1])):
            fbank[j, i] = (i - bin[j]) / (bin[j + 1] - bin[j])
        for i in range(int(bin[j + 1]), int(bin[j + 2])):
            fbank[j, i] = (bin[j + 2] - i) / (bin[j + 2] - bin[j + 1])
    return fbank


def _fbank(frames, sample_rate=16000, filters_num=26, NFFT=512, low_freq=0, high_freq=None):
    """Perform pre-emphasis -> framing -> get magnitude -> FFT -> Mel Filtering.
    Arguments:
        signal: 1-D numpy array.
        sample_rate: Sampling rate. Defaulted to 16KHz.
        win_length: Window length. Defaulted to 0.025, which is 25ms/frame.
        win_step: Interval between the start points of adjacent frames.
            Defaulted to 0.01, which is 10ms.
        filters_num: Numbers of filters. Defaulted to 26.
        NFFT: Size of FFT. Defaulted to 512.
        low_freq: Lowest frequency.
        high_freq: Highest frequency.
        pre_emphasis_coeff: Coefficient for pre-emphasis. Pre-emphasis increase
            the energy of signal at higher frequency. Defaulted to 0.97.
    Returns:
        feat: Features.
        energy: Energy.
    """
    high_freq = high_freq or sample_rate / 2
    spec_power = _spectrum_power(frames, NFFT)
#     print(np.shape(spec_power))
    energy = np.sum(spec_power, 1)
    # 将其中的0全部换掉
    energy = np.where(energy == 0, np.finfo(float).eps, energy)
    # Get Mel filter banks.
    fb = _get_filter_banks(filters_num, NFFT, sample_rate, low_freq, high_freq)
    # Get MFCC and modify all zeros to eps 非负最小值.
    feat = np.dot(spec_power, fb.T)
    # 将其中的0全部换掉
    feat = np.where(feat == 0, np.finfo(float).eps, feat)

    return feat, energy


def _delta(feat, N=2):
    """Compute delta features from a feature vector sequence.
    Arguments:
        feat: A numpy array of size (NUMFRAMES by number of features) containing features.
        Each row holds 1 feature vector.
        N: For each frame, calculate delta features based on preceding and following N frames.
    Returns:
        A numpy array of size (NUMFRAMES by number of features) containing delta features.
        Each row holds 1 delta feature vector.
    """
    NUMFRAMES = len(feat)
    feat = np.concatenate(([feat[0] for i in range(N)], feat, [feat[-1] for i in range(N)]))
    denom = sum([2 * i * i for i in range(1, N + 1)])
    dfeat = []
    for j in range(NUMFRAMES):
        dfeat.append(np.sum([n * feat[N + j + n] for n in range(-1 * N, N + 1)], axis=0) / denom)
    return dfeat


def calcFbank(frames, sample_rate=16000, filters_num=26, NFFT=512, low_freq=0, high_freq=None,
              append_energy=True, append_delta=False):
    """Calculate Fbank Features.
    Arguments:
        signal: 1-D numpy array.
        sample_rate: Sampling rate. Defaulted to 16KHz.
        win_length: Window length. Defaulted to 0.025, which is 25ms/frame.
        win_step: Interval between the start points of adjacent frames.
            Defaulted to 0.01, which is 10ms.
        filters_num: Numbers of filters. Defaulted to 26.
        NFFT: Size of FFT. Defaulted to 512.
        low_freq: Lowest frequency.
        high_freq: Highest frequency.
        pre_emphasis_coeff: Coefficient for pre-emphasis. Pre-emphasis increase
            the energy of signal at higher frequency. Defaulted to 0.97.
        append_energy: Whether to append energy. Defaulted to True.
        append_delta: Whether to append delta to feature. Defaulted to False.
    Returns:
        2-D numpy array with shape (NUMFRAMES, features). Each frame containing filters_num of features.
    """
    (feat, energy) = _fbank(frames, sample_rate, filters_num, NFFT, low_freq, high_freq)
    feat = np.log(feat)
    if append_energy:
        feat[:, 0] = np.log(energy)
    if append_delta:
        feat_delta = _delta(feat)
        feat_delta_delta = _delta(feat_delta)
        feat = np.concatenate((feat, feat_delta, feat_delta_delta), axis=1)

    return feat


from python_speech_features import logfbank
from python_speech_features import fbank

def get_log_fbank(signal, rate):
    return logfbank(signal, rate)
