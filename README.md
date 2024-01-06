# MLOps74
Github repository for Team 74 attending 02476 Machine Learning Operations Jan 24 at DTU.

Project Description Group 74

Project Goal:

This project aims to develop an automated recognition system for
detecting smokers in images using deep learning techniques, and by doing
so we would contribute to environmental health and smart city
monitoring.

Motivation:

The motivation for this project arises from the need for efficient and
automated smoker detection methods around public spaces and common areas
where it is prohibited to smoke or throw away the used cigarette. By
leveraging deep learning, we aim to create a model capable of accurately
classify smoking and non-smoking gestures in images. We aim to ensure a
green environment and enhancing surveillance capabilities in smart
cities.

Data:

Our data consists of a smaller-scale image set containing 1120
preprocessed pictures, evenly split into Smoking and Non-Smoking
classes. These images are gathered by various search engines using
keywords related to cigarette smoking, non-smoking gestures, and
connected activities. The images are versatile for better generalization
of the models, such as smokers from multiple angles and non-smokers
engaged in activities resembling smoking gestures (e.g., drinking water,
using inhaler, coughing). The images have a resolution of 250×250
pixels. For training and validation, 80% of the dataset will be used,
while the remaining 20% will be reserved for testing the model\'s
performance. Additionally for better results we would apply several
transformations on the loaded images such as normalization, resized
crops, rotations and flips, and randomizing these transformations.

Framework and Integration:

To achieve our goal, we plan to utilize the PyTorch deep learning
framework. The main idea is to use a complex Convolutional Neural
Network model. ResNet architectures will be used based on their
performance in handling this image classification challenge. As it is an
easier dataset, we would use simple techniques like sigmoid activation
with BCE loss, and in the end, the valuation would be based on common
metrics such as accuracy, precision, recall and F1 score. The model\'s
training will be optimized to achieve high accuracy in distinguishing
smoking and non-smoking gestures.
