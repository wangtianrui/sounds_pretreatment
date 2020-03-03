import librosa as lib
import matplotlib.pyplot as plt
import numpy as np


def plot(audio):
    plt.plot(audio)
    plt.show()


def add_w_noise(x, snr=15):
    """
    添加白噪声
    :param x:
    :param snr:信噪比 越大噪声越小
    :return:
    """
    noise = np.random.randn(len(x))
    power_x = np.sum(np.abs(x) ** 2)
    power_n = np.sum(np.abs(noise) ** 2)

    noise = np.sqrt(power_x / (10 ** (snr / 10)) / power_n) * noise
    return x + noise


#
# plot(audio)
# audio_wn = add_w_noise(audio)
# plot(audio_wn)

# stft = lib.core.stft(audio)
def fft_study():
    x = np.arange(0, 50, step=0.05)
    sin1 = np.sin(x)
    sin2 = 2 * np.sin(2 * x)
    sin3 = 3 * np.sin(3 * x)

    plt.plot(sin1)
    plt.plot(sin2)
    plt.plot(sin3)
    plt.show()

    mix = sin1 + sin2 + sin3
    plt.plot(mix)
    plt.show()

    stft = lib.core.stft(mix, n_fft=2048)
    print(np.shape(stft))
    # plt.plot(stft[0])
    abs_stft = np.absolute(stft)
    print(abs_stft.shape)
    for index in range(abs_stft.shape[1]):
        plt.plot(abs_stft[:, index][:50])
    plt.show()

    plot(np.mean(abs_stft, axis=1)[:50])


def audio_test(path="./datas/A2_0.wav", add_noise=False):
    audio, frq = lib.load(path)
    audio = audio[36000:53000]

    if add_noise:
        audio = add_w_noise(audio)
    plot(audio)
    print(len(audio) / frq)
    stft = lib.core.stft(audio)
    abs_stft = np.absolute(stft)
    print(abs_stft.shape)
    pre_6 = abs_stft[:, :]
    # print(pre_6.shape)
    for index in range(pre_6.shape[1]):
        plt.plot(pre_6[:, index][100:200])
    plt.show()
    mean = np.mean(pre_6, axis=1)
    plot(mean[:400])
    # temp = np.argsort(mean)[-20:]
    print(np.argsort(mean)[-20:])
    # print(mean[temp])

    # noise = np.random.randn(len(audio))
    # stft_noise = lib.core.stft(noise)
    # abs_noise = np.absolute(stft_noise)
    # for index in range(abs_noise.shape[1]):
    #     plt.plot(abs_noise[:, index][100:200])
    # plt.show()
    # mean = np.mean(abs_noise, axis=1)
    # plot(mean[:400])


if __name__ == '__main__':
    # fft_study()
    # audio_test()
    # 基频决定音高，泛音决定音色。
    # x = [2, 1, 5, 3, 4]
    # print(np.argsort(x))

    # audio_test(r"F:\Traindata\personal voice\nv.mp3", add_noise=False)
    audio_test(r"F:\Traindata\personal voice\nan.mp3", add_noise=True)
