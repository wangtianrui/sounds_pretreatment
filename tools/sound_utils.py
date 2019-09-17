import sounddevice as sd
from IPython.display import Audio


def play_sound(sound_array, freq):
    """
    play a sound
    """
    sd.play(sound_array, freq)
