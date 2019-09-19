import parselmouth
import numpy as np


def get_formant(sound):
    sound = parselmouth.Sound(sound)
    formant = sound.to_formant_burg()
    num_formant = formant.get_number_of_frames()
    formant_ = np.zeros((5, num_formant))
    start_time = formant.start_time
    time_step = formant.get_time_step()
    for i in range(num_formant):
        # 只有前5号共振峰
        formant_[0, i] = formant.get_value_at_time(1, start_time + i * time_step)
        formant_[1, i] = formant.get_value_at_time(2, start_time + i * time_step)
        formant_[2, i] = formant.get_value_at_time(3, start_time + i * time_step)
        formant_[3, i] = formant.get_value_at_time(4, start_time + i * time_step)
        formant_[4, i] = formant.get_value_at_time(5, start_time + i * time_step)
    return formant_
