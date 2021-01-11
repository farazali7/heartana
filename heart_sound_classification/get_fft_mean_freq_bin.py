from scipy.signal import find_peaks
from heart_sound_classification.signal_processing import normalize_signal
import numpy as np


def find_max_peaks(signal, num_peaks=10, height_threshold=0.005, width_threshold=250, height_adjust_level=0.001):
    max_peaks, _ = find_peaks(signal, height=height_threshold, distance=width_threshold)
    iteration_num = 1
    capped_distance = width_threshold
    capped_height = height_threshold
    while len(max_peaks) < num_peaks:
        effective_distance = width_threshold/(10**iteration_num)
        if effective_distance < 1:
            effective_distance = capped_distance
        capped_distance = effective_distance

        effective_height = height_threshold-(height_adjust_level*iteration_num)
        if effective_height < 0:
            effective_height = capped_height
        capped_height = effective_height

        extra_peaks, _ = find_peaks(signal[max_peaks[-1]:], height= effective_height,
                                    distance=effective_distance)
        extra_peaks += max_peaks[-1]
        max_peaks = np.append(max_peaks, extra_peaks)
        iteration_num += 1

    return max_peaks[0:num_peaks]


def get_fft_mean_freq_bin(signal, sampling_frequency):
    real_fft = np.abs(np.fft.rfft(signal))
    real_fft = normalize_signal(real_fft)
    frequency_bins = np.arange(0, len(real_fft)) * (sampling_frequency / len(real_fft))
    peaks = find_max_peaks(real_fft)

    peak_frequency_bins = frequency_bins[peaks]
    mean_peak_frequency_bin = np.mean(peak_frequency_bins)

    return mean_peak_frequency_bin

