from tensorflow.keras.layers import StringLookup
from tensorflow import keras

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os
import re

# 1. Load the training data, randomly arrange it
directory = "./training_images/sorted/"
files = []
for filename in os.listdir(directory):
    if (filename != '.gitignore'):
        files.append(directory+filename)

# Gather the class labels
class_labels = []
for filepath in files:
    filepath = filepath.split('/')[3][:-4]
    filepath = re.sub(pattern=r"[^a-zA-Z]", repl=r"", string=filepath)
    if (filepath not in class_labels):
        class_labels.append(filepath)

np.random.shuffle(files)

# 2. Split the training data into three subsets 90:5:5 (training:validation:test)
train_samples = []
test_samples = []
validation_samples = []

# gets 90:5:5 of each class
for class_label in class_labels:
    class_list = [filepath for filepath in files if class_label in filepath]

    split_idx = int(0.9 * len(class_list))
    train_samples += class_list[:split_idx]
    test_or_val_samples = class_list[split_idx:]

    val_split_idx = int(0.5 * len(test_or_val_samples))
    validation_samples += test_or_val_samples[:val_split_idx]
    test_samples += test_or_val_samples[val_split_idx:]

    print(split_idx, val_split_idx, len(class_list))
    
print(len(train_samples), len(test_samples), len(validation_samples), len(files))

assert len(files) == len(train_samples) + len(validation_samples) + len(
    test_samples
)

print(f"Total training samples: {len(train_samples)}")
print(f"Total validation samples: {len(validation_samples)}")
print(f"Total test samples: {len(test_samples)}")

# a function that gets the image paths and their corresponding labels for whatever array we put in
def get_labels(paths):
    labels = []
    for filepath in paths:
        filepath = filepath.split('/')[3][:-4]
        filepath = re.sub(pattern=r"[^a-zA-Z]", repl=r"", string=filepath)
        labels.append(filepath)
    return paths, labels

train_img_paths, train_labels = get_labels(train_samples)
validation_img_paths, validation_labels = get_labels(validation_samples)
test_img_paths, test_labels = get_labels(test_samples)
