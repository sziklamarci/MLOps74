import torch
from torch.utils.data import DataLoader
from smoke.data.make_dataset import load_images_from_folder, CustomDataset

def test_data():
    # Call load_images_from_folder to get images and labels
    train_images, train_labels = load_images_from_folder('data/raw/archive/Training/Training')
    val_images, val_labels = load_images_from_folder('data/raw/archive/Validation/Validation')

    # Create custom datasets
    train_loader = DataLoader(CustomDataset(train_images, train_labels), shuffle=True)
    val_loader = DataLoader(CustomDataset(val_images, val_labels), shuffle=False)

    assert len(train_loader) == 716
    assert len(val_loader) == 180
    for images, labels in train_loader:
        assert images.size() == torch.Size([1,224,224,3])
        assert len(images) == len(labels)
