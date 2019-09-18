from sidekit.frontend.features import *


def get_plp(signal_array, rate, rasta=True):
    """
    :param signal_array:
    :param rate:
    :param rasta:
    :return:
            [
                cepstra,
                log_energy,
                powspec,
                post_spectrum
            ]
    """
    return plp(signal_array, fs=rate, rasta=rasta)
