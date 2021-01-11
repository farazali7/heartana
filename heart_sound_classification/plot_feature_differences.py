import pickle
import numpy as np
import matplotlib.pyplot as plt


with open("mfp2_heart_sound_features.pickle", "rb") as features:
    heart_sound_features = pickle.load(features)

with open("heart_sound_labels.pickle", "rb") as labels:
    correct_labels = pickle.load(labels)

num_normal = np.count_nonzero(correct_labels == 0)
num_abnormal = np.count_nonzero(correct_labels == 1)

print(num_normal)
print(num_abnormal)

normal_fft_ratio = np.zeros(shape=(num_normal, 1))
normal_cepstrum = np.zeros(shape=(num_normal, 1))
normal_fft_skew = np.zeros(shape=(num_normal, 1))
normal_fft_mean_freq_bin = np.zeros(shape=(num_normal, 1))
normal_energy = np.zeros(shape=(num_normal, 7))
abnormal_fft_ratio = np.zeros(shape=(num_abnormal, 1))
abnormal_cepstrum = np.zeros(shape=(num_abnormal, 1))
abnormal_fft_skew = np.zeros(shape=(num_normal, 1))
abnormal_fft_mean_freq_bin = np.zeros(shape=(num_normal, 1))
abnormal_energy = np.zeros(shape=(num_abnormal, 7))

sample_number_normal = np.zeros(shape=(num_normal,))
sample_number_abnormal = np.zeros(shape=(num_abnormal,))
normal_index = 0
abnormal_index = 0

# Organize all features
for i in range(0, len(heart_sound_features)):
    if correct_labels[i] == 0:
        normal_cepstrum[normal_index] = heart_sound_features[i][0]
        normal_fft_skew[normal_index] = heart_sound_features[i][1]
        normal_energy[normal_index] = heart_sound_features[i][2:9]
        sample_number_normal[normal_index] = i
        normal_index += 1
    elif correct_labels[i] == 1:
        abnormal_cepstrum[abnormal_index] = heart_sound_features[i][0]
        abnormal_fft_skew[abnormal_index] = heart_sound_features[i][1]
        abnormal_energy[abnormal_index] = heart_sound_features[i][2:9]
        sample_number_abnormal[abnormal_index] = i
        abnormal_index += 1


plt.scatter(sample_number_normal, normal_cepstrum[0:], color='blue')
plt.scatter(sample_number_abnormal, abnormal_cepstrum[0:665], color='red')
plt.xlabel("Sample Number")
plt.ylabel("Cepstrum Coefficients Mean")
plt.legend(labels=['Normal', 'Abnormal'])
plt.show()

plt.scatter(sample_number_normal, normal_fft_skew[0:], color='blue')
plt.scatter(sample_number_abnormal, abnormal_fft_skew[0:665], color='red')
plt.xlabel("Sample Number")
plt.ylabel("FFT Skew Value")
plt.legend(labels=['Normal', 'Abnormal'])
plt.show()

fig, axs = plt.subplots(3, 3, figsize=(15, 15))
axs[0, 0].scatter(sample_number_normal, normal_energy[:, 0], color='blue')
axs[0, 0].scatter(sample_number_abnormal, abnormal_energy[:, 0], color='red')
axs[0, 0].set_title('10Hz - 80Hz')

axs[0, 1].scatter(sample_number_normal, normal_energy[:, 1], color='blue')
axs[0, 1].scatter(sample_number_abnormal, abnormal_energy[:, 1], color='red')
axs[0, 1].set_title('80Hz - 150Hz')

axs[0, 2].scatter(sample_number_normal, normal_energy[:, 2], color='blue')
axs[0, 2].scatter(sample_number_abnormal, abnormal_energy[:, 2], color='red')
axs[0, 2].set_title('150Hz - 220Hz')

axs[1, 0].scatter(sample_number_normal, normal_energy[:, 3], color='blue')
axs[1, 0].scatter(sample_number_abnormal, abnormal_energy[:, 3], color='red')
axs[1, 0].set_title('220Hz - 290Hz')

axs[1, 1].scatter(sample_number_normal, normal_energy[:, 4], color='blue')
axs[1, 1].scatter(sample_number_abnormal, abnormal_energy[:, 4], color='red')
axs[1, 1].set_title('290Hz - 360Hz')

axs[1, 2].scatter(sample_number_normal, normal_energy[:, 5], color='blue')
axs[1, 2].scatter(sample_number_abnormal, abnormal_energy[:, 5], color='red')
axs[1, 2].set_title('360Hz - 430Hz')

axs[2, 1].scatter(sample_number_normal, normal_energy[:, 6], color='blue')
axs[2, 1].scatter(sample_number_abnormal, abnormal_energy[:, 6], color='red')
axs[2, 1].set_title('430Hz - 500Hz')

for ax in fig.get_axes():
    ax.set(xlabel='Sample Number', ylabel='Band Energy')

fig.delaxes(axs[2, 0])
fig.delaxes(axs[2, 2])
plt.figlegend(labels=['Normal', 'Abnormal'], loc='lower right')
plt.show()

# plt.scatter(sample_number_normal, normal_fft_skew[0:], color='blue')
# plt.scatter(sample_number_abnormal, abnormal_fft_skew[0:665], color='red')
# plt.xlabel("Sample Number")
# plt.ylabel("FFT Skew Value")
# plt.legend(labels=['Normal', 'Abnormal'])
# plt.show()
#
# plt.scatter(sample_number_normal, normal_fft_mean_freq_bin[0:], color='blue')
# plt.scatter(sample_number_abnormal, abnormal_fft_mean_freq_bin[0:665], color='red')
# plt.xlabel("Sample Number")
# plt.ylabel("FFT Freq Bin Mean")
# plt.legend(labels=['Normal', 'Abnormal'])
# plt.show()