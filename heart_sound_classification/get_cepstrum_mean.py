from python_speech_features import mfcc
import numpy as np


def get_cepstrum_mean(signal, sampling_frequency):
    cepstrum_coefficients = mfcc(signal, samplerate=sampling_frequency)
    average = np.mean(cepstrum_coefficients)

    return average

