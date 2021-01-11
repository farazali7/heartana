[sample-pcg]: ./heart_sound_classification/testing_plots/sample_pcg.png

[model-algorithm]: ./heart_sound_classification/testing_plots/mfp2_algorithm(lfp).png

[hyperplane-example]: ./heart_sound_classification/testing_plots/hyperplane-example.png
[nonlinear-example]: ./heart_sound_classification/testing_plots/nonlinear-example.png

[ccm]: ./heart_sound_classification/testing_plots/cepstrum_coefficients_feature_plot.png
[fftskewval]: ./heart_sound_classification/testing_plots/fft_skew_feature_plot.png
[fftfreqmeanbin]: ./heart_sound_classification/testing_plots/fft_freq_bin_mean_feature_plot.png
[bands]: ./heart_sound_classification/testing_plots/band_energies_feature_plot.png

[confmat1]: ./heart_sound_classification/testing_plots/confusion_matrix_mfp1.png
[roc1]: ./heart_sound_classification/testing_plots/roc_curve_mfp1.png

[confmat2]: ./heart_sound_classification/testing_plots/confusion_matrix_mfp2.png
[roc2]: ./heart_sound_classification/testing_plots/roc_curve_mfp2.png

# Heartana
A machine learning model for classifying heart sounds
as normal or abnormal.

## Problem Definition
Cardiac activities cause vibrations that are transmitted
through tissue to the surface of the chest and thereby form
heart sound signals. These signals can be received by the
human ear or recorded with electronics. A heart sound is
divided into four main segments, the first heart sound
(S1), the second heart sound (S2), the third (S3) and the
fourth (S4). As each sound occurs, the heart changes in its
physiological state. The visual graphing of the heart sound
recording is known as a phonocardiogram (PCG).

<img alt="" src="/heart_sound_classification/testing_plots/sample_pcg.png" width="250px" />

The fundamental heart sounds are usually S1 and S2.
S1 happens at the start of isovolumetric ventricular contraction, 
when the mitral and tricuspid valves close due to the rapid increase in pressure within the ventricles. 
S2 occurs at the start of diastole with the closure of the aortic and pulmonic valves.
The occurrence of other sounds such as S3, S4, systolic clicks,
or diastolic/opening snaps as well as heart murmurs can indicate
different pathological situations.

The goal of the model was to use a dataset provided by the
PhysioNet 2016 Heart Sound Classification challenge, to help
correctly classify input heart sounds as either normal or abnormal.

## Dataset Details

The PhysioNet challenge dataset consists of around 3240 recording samples of heart sounds from individuals 
with normal, healthy hearts, and those with confirmed cardiac conditions. Recordings last from about 5 to 
120 seconds, and the dataset comes with correct labels (normal or abnormal) for each recording. 
Recordings were collected from different places on the body used for regular cardiac auscultations. 
The recordings are of both adults and children in an uncontrolled environment and were resampled to 2kHz. 

## Signal Processing

The signal was first processed by conducting heart sound
segmentation via finding the peaks of the PCG. This helped
to locate the S1, S2, diastole, and systole areas of the
signal. The signal was also processed to remove noise through
a de-noising algorithm.

## Classification Model & Pipeline
The general algorithm design for the model is as follows:
![model-algorithm]

### Feature Extraction
Since heart murmurs occur at higher frequencies than normal heart sounds, the signal’s Fourier transform 
(FT) was inspected. It was hypothesized that the shape of the spectra would be different among normal and 
abnormal signals, as well as the frequency bins showing the most signal activity. The former idea was 
captured within the signal’s FT skew, and the latter was thought to have been shown in the mean frequency 
bin containing the most peaks, as well as through a collection of signal energies. These energies were 
obtained after passing the signal through a bank of 7 bandpass filters uniformly spaced between 100Hz to 500Hz, 
as these frequencies cover most heart sounds. A fourth feature regarding the signal’s power in the time 
domain was also considered, as it was believed that abnormal signals would have higher power due to murmurs. 
To minimize redundancy and comply with requirements of operating on a low-spec device, a feature reduction step 
was completed. The correlation coefficient was found between the features, revealing that the highest correlation 
existed between the band energy collection and mean average frequency bin. The latter was kept due to the former 
requiring longer computation. The average frequency bin feature was later replaced by Mel-Frequency Cepstral
Coefficients (explained later).

### Support Vector Classifier
One of the most frequently used algorithms for binary classification tasks are support vector machines (SVM).
They are centered around the concept of finding the optimal hyperplane (decision boundary) that correctly divides two classes of data points.
A hyperplane for a two dimensional dataset would simply be a one dimensional line as shown below. 
Generally, for N-dimensional data, a hyperplane is just an N-1 dimensional subspace.

![hyperplane-example]

The SVM algorithm works by first identifying the support vectors to be used for a hyperplane. From these support vectors, the margin, which is the perpendicular distance from the hyperplane to the support vectors, is calculated.
It is worth noting that when some misclassifications are allowed, such as allowing a vector to reside on the wrong side of the decision boundary, the SVM’s margin is known as a soft margin.
Comparatively, a hard margin approach is used when no misclassified training vectors are allowed to exist.
The goal of the algorithm is to maximize this margin to ensure that new observations have greater chance of falling on the correct side of the hyperplane, and thereby being correctly classified.
Choosing the hyperplane that maximizes this margin becomes a simple optimization problem. Different hyperplanes, that vary by their chosen support vectors, are iteratively compared to find the one that produces the maximum margin. Based on the location of new data with respect to the optimal hyperplane, it is classified into one of the two classes associated with its location.
In the case of using nonlinear data, different mapping functions can be used to transform the data into higher dimensions.

![nonlinear-example]

This enables the SVM to then find an adequate hyperplane for classification. However, since input data can have a high number of features, it can be computationally expensive to directly apply these mapping functions.
In this case, an SVM employs a kernel trick, where it uses a simpler function (kernel) in the original space and then computes the dot product, achieving the same data transformation, avoiding the need for an exhaustive mapping function to first be applied.

## Results
Each iteration of the prototype was trained using 10-fold cross validation. This was to ensure that the 
support vector classifier would not overfit to the dataset used. Since the training and testing accuracies 
within each iteration were similar, it was confirmed that the model was not experiencing any severe overfitting.
The false negatives of the first iteration were higher than the second iteration. In the given problem 
context, this had to be minimized since it is critical in the healthcare domain that a patient with heart 
abnormalities is correctly made aware of their condition. Thus, the actual classification ability of the 
binary classifier was evaluated using ROC curves.

### Feature Plots
![ccm]

![fftskewval]

![fftfreqmeanbin]

![bands]

Notes:
- Feature Usage
    - Cepstrum Coefficients Mean (Prototype 1, Prototype2)
    - FFT Skew Value (Prototype 1, Prototype 2)
    - FFT Frequency Bin Mean (Prototype 1)
    - Band Energies (7 bands = 7 features) (Prototype2)
- The first 800-900ish data points shown in each feature plot are of the noisiest, most difficult recordings from the entire dataset. They are organized first here only for the purposes of showing a bit more clearly on these graphs what the delineation of features looks like for very noisy data. The rest of the data points are from fairly normal recordings (no insane amount of noise but still some).
- FFT Frequency Bin Mean was replaced from Prototype 1 due to most lack of delineation seen between normal and abnormal data points in their plots.


### Prototype 1

- Average 10-fold CV Accuracy = 85.9%
- Testing Accuracy = 85.2%

![confmat1]

![roc1]

Notes:
- Positive = Abnormal heart sound
- Negative = Normal heart sound 
- For this model, the accuracy itself seems to be decent as benchmark is technically exceeded (80%)
- Train Accuracy ≈ Test Accuracy so model does not overfit which is good
- Taking a closer look at confusion matrix shows very low sensitivity because of low True Positives. This means the model is not great at classifying abnormal heart sounds. 
- High specificity here =  good at confirming normal heart sounds 
- Need to work on increasing overall accuracy and sensitivity, since sensitivity is very important in diagnosing patient correctly
- ROC curve not that great... AUC > 0.5 (threshold) so it is a bit better than randomly guessing



### Prototype 2

- Average 10-fold CV Accuracy = 86.6%
- Testing Accuracy = 86.3%

![confmat2]

![roc2]

Notes:
- Positive = Abnormal heart sound
- Negative = Normal heart sound 
- Benchmark accuracy exceeded
- Train Accuracy ≈ Test Accuracy so model does not overfit which is good
- Higher sensitivity now means model is better than last at classifying abnormal heart sounds
- High specificity here =  good at confirming normal heart sounds 
- Can still improve by reducing False Negatives (second highest metric in confusion matrix), these are also dangerous in the context of the SOC where a patient thinks they are fine but in reality they are not
- ROC curve is better and AUC is approaching one indicating better classifier performance
