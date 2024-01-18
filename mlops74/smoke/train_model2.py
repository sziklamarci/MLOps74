import torch
import torch.nn as nn
from torch.optim.lr_scheduler import MultiStepLR
from torch.utils.data import DataLoader
from data.make_dataset import CustomDataset
from models.model import MyNeuralNet
from tqdm import tqdm
import numpy as np

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Create data loaders
train_loader = DataLoader(torch.load("mlops74/data/processed/Training/train_dataset.pt"), batch_size=64, shuffle=True)
val_loader = DataLoader(torch.load("mlops74/data/processed/Validation/val_dataset.pt"), batch_size=64, shuffle=False)

# Createing the model with MyResNet class
model = MyNeuralNet(num_classes=2).to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
learning_rate = 0.0001
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
lr_milestones = [7, 14, 21, 28, 35]
multi_step_lr_scheduler = MultiStepLR(optimizer, milestones=lr_milestones, gamma=0.1)

# Early stopping
patience = 3
counter = 0
best_loss = np.inf

# Training loop with logging
EPOCHS = 10
logs = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}

model.to(device)

for epoch in tqdm(range(EPOCHS)):
    model.train()
    train_loss = 0.0
    correct_train = 0
    total_train = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        _, predicted_train = torch.max(outputs, 1)
        total_train += labels.size(0)
        correct_train += (predicted_train == labels).sum().item()

    train_accuracy = correct_train / total_train

    # Validation
    model.eval()
    with torch.no_grad():
        val_loss = 0.0
        correct_val = 0
        total_val = 0
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

            _, predicted_val = torch.max(outputs, 1)
            total_val += labels.size(0)
            correct_val += (predicted_val == labels).sum().item()

        val_accuracy = correct_val / total_val

    # Adjust learning rate
    multi_step_lr_scheduler.step()

    # Logging
    logs['train_loss'].append(train_loss / len(train_loader))
    logs['train_acc'].append(train_accuracy)
    logs['val_loss'].append(val_loss / len(val_loader))
    logs['val_acc'].append(val_accuracy)

    print(f'EPOCH: {epoch + 1}/{EPOCHS} \
    train_loss: {train_loss / len(train_loader):.4f}, train_acc: {train_accuracy:.3f} \
    val_loss: {val_loss / len(val_loader):.4f}, val_acc: {val_accuracy:.3f} \
    Learning Rate: {optimizer.param_groups[0]["lr"]}')

    torch.save(model.state_dict(), "mlops74/models/checkpoints/last.pth")
    # Check for improvement and apply early stopping
    if val_loss < best_loss:
        counter = 0
        best_loss = val_loss
        torch.save(model.state_dict(), "mlops74/models/checkpoints/best.pth")
    else:
        counter += 1

    if counter >= patience:
        print("Early stopping!")
        break
