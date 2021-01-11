import soundfile as sf
import glob, os, csv, pickle
import numpy as np


def load_heart_sounds_and_labels(paths):

    total_audio_data = []
    correct_label_dict = {}
    correct_labels = []
    for path in paths:

        with open(os.path.join(path, "REFERENCE.csv")) as label_csv:
            csv_reader = csv.reader(label_csv, delimiter=',')
            for row in csv_reader:
                value = int(row[1])
                if value == -1:  # PhysioNet labels normal heart sounds as -1 so we convert to 0
                    value += 1
                correct_label_dict[row[0]] = value

        all_files = glob.glob(os.path.join(path, "*.wav"))
        for audio_file in all_files:
            audio, sampling_freq = sf.read(audio_file)
            total_audio_data.append(audio)
            file_name = os.path.splitext(os.path.basename(audio_file))[0]
            label = correct_label_dict[file_name]
            correct_labels.append(label)

    total_audio_data = np.array(total_audio_data)
    correct_labels = np.array(correct_labels)

    return total_audio_data, correct_labels


# Generate data and labels for model training/testing
paths = ["../sample_heart_sounds/set-a", "../sample_heart_sounds/set-b", "../sample_heart_sounds/set-c", "../sample_heart_sounds/set-d", "../sample_heart_sounds/set-e", "../sample_heart_sounds/set-f"]
audio, labels = load_heart_sounds_and_labels(paths)

with open("heart_sound_data.pickle", "wb") as heart_sound_data:
    pickle.dump(audio, heart_sound_data)

with open("heart_sound_labels.pickle", "wb") as heart_sound_labels:
    pickle.dump(labels, heart_sound_labels)






