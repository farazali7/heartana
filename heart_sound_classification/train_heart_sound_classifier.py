from sklearn.model_selection import cross_val_score, StratifiedKFold, train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns


with open("mfp2_heart_sound_features.pickle", "rb") as features:
    train_heart_sound_features = pickle.load(features)

with open("heart_sound_labels.pickle", "rb") as labels:
    train_labels = pickle.load(labels)

# Scale input features for proper comparison in model
scaler = StandardScaler()
print(train_heart_sound_features.shape)
train_heart_sound_features = scaler.fit_transform(train_heart_sound_features)

# Split into train-test sets
features_train, features_test, labels_train, labels_test = train_test_split(train_heart_sound_features, train_labels, test_size=0.2, random_state=1, stratify=train_labels)

# Create classifier
heart_sound_classifier = SVC(probability=True)

# Train and evaluate
scores = cross_val_score(heart_sound_classifier, train_heart_sound_features, train_labels, cv=StratifiedKFold(n_splits=10, shuffle=True))
print("SVC Cross Validation Scores", format(scores))
print("SVC Average Score: ", format(np.mean(scores)))


heart_sound_classifier.fit(features_train, labels_train)
test_score = heart_sound_classifier.score(features_test, labels_test)
print("SVC Test Score: ", format(test_score))

predicted_labels = heart_sound_classifier.predict(features_train)
confusion_matrix = confusion_matrix(labels_train, predicted_labels)

ax = plt.subplot()
sns.heatmap(confusion_matrix, annot=True, ax=ax, cmap='Greens', fmt='g')
ax.set_xlabel('Predicted labels')
ax.set_ylabel('True labels')
ax.set_title('Confusion Matrix')
ax.xaxis.set_ticklabels(['Normal', 'Abnormal'])
ax.yaxis.set_ticklabels(['Normal', 'Abnormal'])
plt.show()

print(labels_test)
print(predicted_labels)

true_negatives, false_positives, false_negatives, true_positives = confusion_matrix.ravel()

print("True negatives: ", format(true_negatives))
print("True positives: ", format(true_positives))
print("False negatives: ", format(false_negatives))
print("False positives: ", format(false_positives))

sensitivity = (true_positives / (true_positives + false_negatives)) * 100
specificity = (true_negatives / (true_negatives + false_positives)) * 100
accuracy = ((true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)) *100

print("Accuracy: ", format(accuracy))
print("Sensitivity: ", format(sensitivity))
print("Specificity: ", format(specificity))


# Create ROC plot w/ area under curve calculated
predicted_label_prob = heart_sound_classifier.predict_proba(features_test)[:,1]
area_under_curve = roc_auc_score(labels_test, predicted_label_prob)
fpr, tpr, thresholds = roc_curve(labels_test, predicted_label_prob)
plt.plot(fpr, tpr, label='ROC curve')
plt.plot([0, 1], [0, 1], 'k--', label='Random guess')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.xlim([-0.02, 1])
plt.ylim([0, 1.02])
plt.legend(loc="lower right")
plt.text(0.7, 0.2, 'AUC = %0.4f' % area_under_curve)
plt.show()

# # Save best performing model
# with open('mfp2_heart_sound_classifier.pkl', 'wb') as hsc:
#     pickle.dump(heart_sound_classifier, hsc)

