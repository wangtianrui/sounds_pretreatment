from scipy.io import wavfile


def get_audio(path=r"../datas/A2_0.wav"):
    return wavfile.read(path)
