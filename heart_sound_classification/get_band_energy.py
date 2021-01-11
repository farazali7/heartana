from heart_sound_classification.signal_processing import butter_bandpass_filter, normalize_signal
import numpy as np


def get_band_energy(signal, sampling_frequency, start_value, final_value, band_width):
        start_band = start_value
        end_band = start_band + band_width
        band_energies = []
        while (end_band <= final_value):
            band_filtered_signal = butter_bandpass_filter(signal, start_band, end_band, sampling_frequency, order=6)
            normalized_filtered_signal = normalize_signal(band_filtered_signal)
            energy = np.sum(np.square(np.abs(normalized_filtered_signal)))
            band_energies.append(energy)
            start_band = end_band
            end_band += band_width

        return band_energies

