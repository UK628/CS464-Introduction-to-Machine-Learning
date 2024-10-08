# -*- coding: utf-8 -*-
"""q3main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10q1DePkqen2IuH-guVeGejxqlHnWWhmK

# Data Preprocessing Tools

## Importing the libraries
"""

import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

"""## Importing the dataset"""

X_train_dataset = pd.read_csv('X_train.csv', delim_whitespace=True)
Y_train_dataset = pd.read_csv('y_train.csv',header=None)
X_test_dataset = pd.read_csv('X_test.csv', delim_whitespace=True)
Y_test_dataset = pd.read_csv('y_test.csv',header=None)
X_train_values = X_train_dataset.values
Y_train_values = Y_train_dataset.values
X_test_values = X_test_dataset.values
Y_test_values = Y_test_dataset.values

Y_test_dataset.rename(columns={0: 'label'}, inplace=True)

"""## Calculating the Percentages"""

#Function to calculate category counts in y_test and y_train
def calculate_category_counts(Y_values):
    category_counts = [0, 0, 0, 0, 0]

    for i in range(Y_values.shape[0]):
        category = Y_values[i][0]
        if category >= 0 and category <= 4:
            category_counts[category] += 1

    return category_counts

category_test_counts = calculate_category_counts(Y_test_values)
print(category_test_counts)

category_train_counts = calculate_category_counts(Y_train_dataset.values)
print(category_train_counts)

"""## Drawing Pie Chart"""

# Data for the pie charts
labels = ['Category 0', 'Category 1', 'Category 2', 'Category 3', 'Category 4']

# Plotting the pie charts in a single frame
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Train data pie chart
ax1.pie(category_train_counts, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.set_title('Distribution of Categories in Y_train_values')

# Test data pie chart
ax2.pie(category_test_counts, labels=labels, autopct='%1.1f%%', startangle=90)
ax2.set_title('Distribution of Categories in Y_test_values')

plt.show()

"""## Calculating Prior Probabilities"""

def calculate_prior_probabilities(category_counts, total_samples):
    prior_probabilities = [count / total_samples for count in category_counts]
    return prior_probabilities

total_train_samples = Y_train_values.shape[0]
prior_train_probabilities = calculate_prior_probabilities(category_train_counts, total_train_samples)
print(prior_train_probabilities)

total_test_samples = Y_test_values.shape[0]
prior_test_probabilities = calculate_prior_probabilities(category_test_counts, total_test_samples)
print(prior_test_probabilities)

"""## Calculating Word Frequencies"""

def calculate_word_frequency(word, label, X_dataset, Y_dataset):
    word_frequency = 0
    column_index = X_dataset.columns.get_loc(word)

    for i in range(X_dataset.shape[0]):
        if Y_dataset.values[i][0] == label:
            word_frequency += X_dataset.iloc[i, column_index]

    return word_frequency

frequency_alien = calculate_word_frequency('alien', 4 , X_train_dataset, Y_train_dataset)
print(frequency_alien)

frequency_thunder = calculate_word_frequency('thunder', 4 , X_train_dataset, Y_train_dataset)
print(frequency_thunder)

"""## Train Multinomial Naive Bayes"""

def train_multinomial_naive_bayes(X_train, Y_train, prior_train_probabilities):
    num_classes = 5
    num_words = X_train.shape[1]

    theta = np.zeros((num_words, num_classes))
    pi = np.zeros(num_classes)

    for yk in range(num_classes):
        pi[yk] = prior_train_probabilities[yk]

        class_indices = (Y_train == yk)
        Tj_yk_array = X_train[class_indices].sum(axis=0)

        Tj_yk_sum = Tj_yk_array.sum()

        theta[:, yk] = np.where(Tj_yk_array == 0, 0, (Tj_yk_array) / (Tj_yk_sum))
    print()
    return theta, pi

theta, pi = train_multinomial_naive_bayes(X_train_dataset, Y_train_dataset.values.flatten(), prior_train_probabilities)

print(theta)

def predict_multinomial_naive_bayes(X_test, theta, pi):
    num_classes = theta.shape[1]
    num_words = theta.shape[0]

    log_theta = np.log(theta)

    scores = np.dot(X_test.values, log_theta) + np.log(pi)

    predictions = np.argmax(scores, axis=1)

    return predictions

"""## Test Multinomial Naive Bayes"""

def calculate_accuracy(predictions, true_labels):
    correct_predictions = 0
    total_instances = len(predictions)

    for i in range(total_instances):
        if predictions[i] == true_labels[i]:
            correct_predictions += 1

    accuracy = correct_predictions / total_instances
    return accuracy

def calculate_confision_matrix(true_labels, predictions):
  conf_matrix = confusion_matrix(true_labels, predictions)
  print("Confusion Matrix:")
  print(conf_matrix)

  # Visualize confusion matrix
  plt.figure(figsize=(8, 6))
  sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", cbar=False,
              xticklabels=["Class {}".format(i) for i in range(conf_matrix.shape[1])],
              yticklabels=["Class {}".format(i) for i in range(conf_matrix.shape[0])])
  plt.xlabel('Predicted')
  plt.ylabel('True')
  plt.title('Confusion Matrix')
  plt.show()

predictions = predict_multinomial_naive_bayes(X_test_dataset, theta, pi)
accuracy = calculate_accuracy(predictions, Y_test_dataset.values.flatten())
print(f"Accuracy: {accuracy:.3f}")
calculate_confision_matrix(Y_test_dataset.values, predictions)

"""## Train Multinomial Naive Bayes With Smoothing"""

def train_multinomial_naive_bayes_with_smoothing(X_train, Y_train, prior_train_probabilities):
    num_classes = 5
    num_words = X_train.shape[1]

    theta = np.zeros((num_words, num_classes))
    pi = np.zeros(num_classes)

    for yk in range(num_classes):
        pi[yk] = prior_train_probabilities[yk]

        class_indices = (Y_train == yk)
        Tj_yk_array = X_train[class_indices].sum(axis=0)

        Tj_yk_sum = Tj_yk_array.sum()

        theta[:, yk] = np.where(Tj_yk_array == 0, 0, (Tj_yk_array + 1.0) / (Tj_yk_sum + num_words))

    return theta, pi

theta, pi = train_multinomial_naive_bayes_with_smoothing(X_train_dataset, Y_train_dataset.values.flatten(), prior_train_probabilities)

"""## Test Multinomial Naive Bayes With Smoothing"""

def predict_multinomial_naive_bayes_with_smoothing(X_test, theta, pi):
    num_classes = theta.shape[1]
    num_words = theta.shape[0]

    log_theta = np.log(theta + (1.0/num_words))

    scores = np.dot(X_test.values, log_theta) + np.log(pi)

    predictions = np.argmax(scores, axis=1)

    return predictions

predictions = predict_multinomial_naive_bayes_with_smoothing(X_test_dataset, theta, pi)
accuracy = calculate_accuracy(predictions, Y_test_dataset.values.flatten())
print(f"Accuracy: {accuracy:.3f}")
calculate_confision_matrix(Y_test_dataset.values, predictions)

"""## Train Bernoulli Naive Bayes"""

def train_bernoulli_naive_bayes(X_train, Y_train, prior_train_probabilities, alpha=1):
    num_classes = 5
    num_words = X_train.shape[1]

    theta = np.zeros((num_words, num_classes))
    pi = np.zeros(num_classes)

    for yk in range(num_classes):
        yk_indices = (Y_train == yk)
        Nyk_array = np.sum(yk_indices)

        pi[yk] = prior_train_probabilities[yk]
        # Apply binarization to X_train
        X_train_bin = np.where(X_train > 0, 1, 0)

        # Use binarized matrix in the summation
        Sj_yk_array = X_train_bin[yk_indices].sum(axis=0)
        theta[:, yk] = (Sj_yk_array + alpha) / (Nyk_array + 2 * alpha)

    return theta, pi

theta, pi = train_bernoulli_naive_bayes(X_train_dataset, Y_train_dataset.values.flatten(), prior_train_probabilities)

def predict_bernoulli_naive_bayes(X_test, theta, pi):
    num_classes = theta.shape[1]
    num_words = theta.shape[0]
    X_binary = (X_test > 0).astype(int)

    # Use the logarithmic probabilities calculated during training
    log_theta = np.log(theta)
    log_not_theta = np.log(1 - theta)

    # Initialize scores with logarithmic priors
    scores = np.log(pi) + np.dot(X_binary.values, log_theta) + np.dot(1 - X_test.values, log_not_theta)

    # Choose the class with the highest score
    predictions = np.argmax(scores, axis=1)

    return predictions

"""## Test Bernoulli Naive Bayes With Smoothing"""

predictions = predict_bernoulli_naive_bayes(X_test_dataset, theta, pi)
accuracy = calculate_accuracy(predictions, Y_test_dataset.values.flatten())
print(f"Accuracy: {accuracy:.3f}")
calculate_confision_matrix(Y_test_dataset.values, predictions)