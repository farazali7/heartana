from heart_sound_classification.get_fft_response_ratio import get_fft_response_ratio
from heart_sound_classification.get_band_energy import get_band_energy
from heart_sound_classification.get_cepstrum_mean import get_cepstrum_mean
from heart_sound_classification.get_fft_skew import get_fft_skew
from heart_sound_classification.get_fft_mean_freq_bin import get_fft_mean_freq_bin
from heart_sound_classification.signal_processing import butter_bandpass_filter, normalize_signal, standardize_signal
import pickle
import numpy as np


def get_heart_sound_features(heart_recordings, sampling_frequency, feature_list):
    # Get total number of features
    num_features = len(feature_list)
    if 'band_energies' in feature_list:
        num_features += 6
    total_features = np.zeros(shape=(len(heart_recordings), num_features))
    index = 0

    for heart_sound in heart_recordings:
        # Standardize + filter audio
        filtered_heart_sound = butter_bandpass_filter(heart_sound, 25, 450, sampling_frequency)
        normalized_heart_sound = standardize_signal(filtered_heart_sound)  # Scale to -1 to 1 instead of 0 to 1

        heart_sound_features = []
        if 'fft_ratio' in feature_list:
            heart_sound_features.append(get_fft_response_ratio(normalized_heart_sound))
        if 'cepstrum_mean' in feature_list:
            heart_sound_features.append(get_cepstrum_mean(normalized_heart_sound, sampling_frequency))
        if 'fft_skew' in feature_list:
            heart_sound_features.append(get_fft_skew(heart_sound))
        if 'fft_mean_freq_bin' in feature_list:
            heart_sound_features.append(get_fft_mean_freq_bin(heart_sound, sampling_frequency))
        if 'band_energies' in feature_list:
            energies = (get_band_energy(heart_sound, sampling_frequency, 10, 500, 70))
            for band_energy in energies:
                heart_sound_features.append(band_energy)

        total_features[index] = heart_sound_features

        index += 1

    return total_features


with open("heart_sound_data.pickle", "rb") as heart_sound_data:
    heart_sounds = pickle.load(heart_sound_data)

sampling_frequency = 2000.0
feature_list = ['fft_skew', 'band_energies', 'cepstrum_mean']
heart_sound_features = get_heart_sound_features(heart_sounds, sampling_frequency, feature_list)


with open("mfp2_heart_sound_features.pickle", "wb") as features:
    pickle.dump(heart_sound_features, features)






