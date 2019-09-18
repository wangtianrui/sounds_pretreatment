import parselmouth
import numpy as np


def get_formant(sound):
    sound = parselmouth.Sound(sound)
    formant = sound.to_formant_burg()
    num_formant = formant.get_number_of_frames()
    formant_ = np.zeros((num_formant, 5))
    start_time = formant.start_time
    time_step = formant.get_time_step()
    for i in range(num_formant):
        formant_[i, 0] = formant.get_value_at_time(1, start_time + i * time_step)
        formant_[i, 1] = formant.get_value_at_time(2, start_time + i * time_step)
        formant_[i, 2] = formant.get_value_at_time(3, start_time + i * time_step)
        formant_[i, 3] = formant.get_value_at_time(4, start_time + i * time_step)
        formant_[i, 4] = formant.get_value_at_time(5, start_time + i * time_step)
    return formant_
