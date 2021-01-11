import numpy as np
from scipy.stats import skew
from heart_sound_classification.signal_processing import normalize_signal


def get_fft_skew(signal):
    real_fft = np.abs(np.fft.rfft(signal))
    real_fft = normalize_signal(real_fft)

    fft_skew = skew(real_fft)

    return fft_skew

