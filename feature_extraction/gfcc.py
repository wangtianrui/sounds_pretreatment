from feature_extraction.gammatone_gram import gammatonegram
import numpy as np


def get_gfcc(audio, rate, log_constant=1e-80, db_threshold=-50.):
    sxx, center_freq = gammatonegram(audio, sr=rate, fmin=20, fmax=int(rate / 2.))
    sxx[sxx == 0] = log_constant
    sxx = 20.0 * np.log10(sxx)  # to db
    sxx[sxx < db_threshold] = db_threshold
    return sxx, center_freq
