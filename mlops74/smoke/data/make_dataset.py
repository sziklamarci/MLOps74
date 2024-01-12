import os
import cv2
import numpy as np
import scikit

def load_images_from_folder(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img = cv2.resize(img, (224, 224))  # Resize images
            img = img / 255.0  # Normalize images
            images.append(img)
            label = 1 if 'smoking' in filename else 0  # Extract label from filename
            labels.append(label)
    return np.array(images), np.array(labels)

def process_data():
    train_images, train_labels = load_images_from_folder('/mlops74/data/raw/Training')
    val_images, val_labels = load_images_from_folder('/mlops74/data/raw/Validation')
    test_images, test_labels = load_images_from_folder('/mlops74/data/raw/Test')

    return (train_images, train_labels), (val_images, val_labels), (test_images, test_labels)

if __name__ == '__main__':
    (train_images, train_labels), (val_images, val_labels), (test_images, test_labels) = process_data()
    
    # Now you can use these datasets for training and evaluating your model
