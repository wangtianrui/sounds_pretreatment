import sounddevice as sd


def play_sound(sound_array, freq):
    """
    play a sound
    """
    sd.play(sound_array, freq)
