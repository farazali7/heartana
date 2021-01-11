import numpy as np


def get_fft_response_ratio(signal):
    fast_fourier_transform = np.fft.rfft(signal)
    max_value = np.max(fast_fourier_transform)
    mean_value = np.mean(fast_fourier_transform)
    fft_ratio = mean_value/max_value

    return abs(fft_ratio)
