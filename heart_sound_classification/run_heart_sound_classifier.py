import pickle
import soundfile as sf
from heart_sound_classification.feature_extractor import get_heart_sound_features


def make_prediction(heart_sound):
    with open('mfp2_heart_sound_classifier.pkl', 'rb') as heart_sound_classifier:
        classifier = pickle.load(heart_sound_classifier)

    features = get_heart_sound_features([heart_sound], sampling_frequency,
                                        ['fft_skew', 'fft_mean_freq_bin', 'cepstrum_mean'])

    prediction_value = classifier.predict(features)

    if prediction_value == 1:
        prediction = 'Abnormal heart conditions found.'
    elif prediction_value == 0:
        prediction = 'Normal heart conditions.'

    return prediction


# Test heart sound
test_path = '../sample_heart_sounds/set-a/a0007.wav'
test_heart_sound, sampling_frequency = sf.read(test_path)

prediction = make_prediction(test_heart_sound)

print(prediction)

