import torch
from torchvision import transforms
from torch.utils.data import DataLoader
from smoke.data.make_dataset import load_images_from_folder, CustomDataset # Run the tests from mlops74 directory
import pytest
import os.path

@pytest.mark.skipif(not os.path.exists('/Users/macbookpro/MLOps74/mlops74/data/raw/archive/Training'), reason="Data files not found")

def test_data():
    train_images, train_labels = load_images_from_folder('mlops74/data/raw/archive/Training/Training')
    val_images, val_labels = load_images_from_folder('mlops74/data/raw/archive/Validation/Validation')

    transform_train = transforms.Compose([
        transforms.ToTensor(),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomErasing(p=0.5, scale=(0.1,0.15)),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_loader = DataLoader(CustomDataset(train_images, train_labels, transform=transform_train), shuffle=True)
    val_loader = DataLoader(CustomDataset(val_images, val_labels, transform=transform_train), shuffle=False)

    # Test 1: Check if the length of the train_loader is correct
    assert len(train_loader) == 716, "Trainloader did not have the correct number of samples"

    # Test 2: Check if the length of the val_loader is correct
    assert len(val_loader) == 180, "Validation set did not have the correct number of samples"

    # Test 3: Check the shape of images from train_loader
    for images, labels in train_loader:
        assert images.size() == torch.Size([1, 3, 224, 224]) # Batch size, channels, height, width

    # Test 4: Check if the number of images and labels are the same
        assert len(images) == len(labels)

    # Test 5: Check if the labels are within the expected range (0 or 1)
        assert all(label.item() in [0, 1] for label in labels)

    # Test 6: Check if the number of unique labels in the validation set is correct
        unique_val_labels = torch.unique(torch.tensor(val_labels))
        assert len(unique_val_labels) == 2

