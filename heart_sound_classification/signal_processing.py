import numpy as np
from scipy.signal import butter, filtfilt


def standardize_signal(input_signal):
    signal_mean = np.mean(input_signal)
    signal_std_dev = np.std(input_signal)
    standardized_signal = np.divide(np.subtract(input_signal, signal_mean), signal_std_dev)

    return standardized_signal


def normalize_signal(input_signal):
    return np.divide(np.subtract(input_signal, np.min(input_signal)), np.subtract(np.max(input_signal), np.min(input_signal)))


def butter_bandpass(lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')

    return b, a


def butter_bandpass_filter(data, lowcut, hightcut, fs, order=6):
    b, a = butter_bandpass(lowcut, hightcut, fs)
    y = filtfilt(b, a, data)

    return y