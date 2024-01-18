import os
import cv2
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import torchvision.transforms.functional as F
import matplotlib.pyplot as plt

class CustomDataset(Dataset):
    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img = self.images[idx]
        label = self.labels[idx]

        if self.transform:
            img = self.transform(img)

        return img, torch.tensor(label, dtype=torch.int64)

def load_images_from_folder(folder):
    images = []
    labels = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            img = cv2.imread(file_path)
            if img is not None:
                img = cv2.resize(img, (224, 224))  # Resize images
                #img = img / 255.0  # Normalize images
                images.append(img)
                
                # Extract label from filename based on starting with 'smoking' or 'notsmoking'
                if filename.lower().startswith('smoking'):
                    label = 1
                elif filename.lower().startswith('notsmoking'):
                    label = 0
                labels.append(label)
    print(f"Number of images: {len(images)}, Number of labels: {len(labels)}")
    return np.array(images), np.array(labels)

    
def process_data():
    train_images, train_labels = load_images_from_folder('mlops74/data/raw/archive/Training/Training')
    val_images, val_labels = load_images_from_folder('mlops74/data/raw/archive/Validation/Validation')
    test_images, test_labels = load_images_from_folder('mlops74/data/raw/archive/Testing/Testing')

    return (train_images, train_labels), (val_images, val_labels), (test_images, test_labels)

if __name__ == '__main__':

    (train_images, train_labels), (val_images, val_labels), (test_images, test_labels) = process_data()

    # If we want we can have some more transformations included
    transform_train = transforms.Compose([
        transforms.ToTensor(),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomErasing(p=0.5, scale=(0.1,0.15)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Create custom datasets
    train_dataset = CustomDataset(train_images, train_labels, transform=transform_train)
    val_dataset = CustomDataset(val_images, val_labels, transform=transform_train)
    test_dataset = CustomDataset(test_images, test_labels, transform=transform_test)

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

    torch.save(train_dataset, "data/processed/Training/train_dataset.pt")
    torch.save(val_dataset, "data/processed/Validation/val_dataset.pt")
    torch.save(test_dataset, "data/processed/Testing/test_dataset.pt")

    # Check the length after loading
    #print("Length of train_dataset after loading:", len(train_images), len(train_labels))

    '''# Get a random batch from the train_loader
    for batch in train_loader:
        images, labels = batch
        break  # Break to get only the first batch

    # Select a random index within the batch
    random_index = np.random.randint(len(images))

    # Extract the random image tensor
    random_image = images[random_index]

    # Display the image using torchvision
    plt.imshow(F.to_pil_image(random_image))
    plt.title(f"Label: {labels[random_index].item()}")
    plt.show()'''

