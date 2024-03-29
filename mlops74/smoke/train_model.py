import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from sklearn.metrics import precision_score, recall_score, f1_score
from data.make_dataset import CustomDataset, process_data
from models.model import MyNeuralNet

import os
import hydra
from omegaconf import OmegaConf
import wandb

@hydra.main(config_path="config", config_name="default_config.yaml")
def train(config):
    print(f"configuration: \n {OmegaConf.to_yaml(config)}")
    
    wandb.init(project="project_mlops74", name="mlops74")

    hparams = config.experiment
    torch.manual_seed(hparams["seed"])

    # Set the working directory to the project root
    hydra_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    os.chdir(hydra_root)
    print(f"Working directory set to: {hydra_root}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # Create an instance of MyNeuralNet
    model = MyNeuralNet()
    # Move the model to the specified device
    model.to(device)

    (train_images, train_labels), (val_images, val_labels), _ = process_data()

    transform_train = transforms.Compose([
        transforms.ToTensor(),
        transforms.RandomVerticalFlip(p=hparams["p_RandomVerticalFlip"]),
        transforms.RandomHorizontalFlip(p=hparams["p_RandomHorizontalFlip"]),
        transforms.RandomErasing(p=hparams["p_RandomErasing"], scale=list(hparams["scale_RandomErasing"])),
        transforms.Normalize(mean=hparams["mean_Normalize"], std=hparams["std_Normalize"])
    ])

    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=hparams["mean_Normalize"], std=hparams["std_Normalize"])
    ])

    train_dataset = CustomDataset(train_images, train_labels, transform=transform_train)
    val_dataset = CustomDataset(val_images, val_labels, transform=transform_test)

    train_loader = DataLoader(train_dataset, batch_size=hparams["batch_size"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=hparams["batch_size"], shuffle=False)

    criterion = nn.CrossEntropyLoss()  # Use CrossEntropyLoss for classification tasks
    optimizer = optim.Adam(model.parameters(), lr=hparams["lr"])

    for epoch in range(hparams["n_epochs"]):
        # Training
        model.train()
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            wandb.log({"train_loss": loss.item()})  # Log training loss

        # Validation
        model.eval()
        with torch.no_grad():
            val_loss = 0.0
            correct = 0
            total = 0
            all_predictions = []
            all_labels = []
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                all_predictions.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

            precision = precision_score(all_labels, all_predictions, average='macro')
            recall = recall_score(all_labels, all_predictions, average='macro')
            f1 = f1_score(all_labels, all_predictions, average='macro')

            wandb.log({"val_loss": val_loss / len(val_loader), "accuracy": (correct / total) * 100,
                       "precision": precision, "recall": recall, "f1_score": f1})  # Log additional metrics

            print(f"Epoch {epoch + 1}/{hparams['n_epochs']}, Loss: {val_loss / len(val_loader)}, "
                  f"Accuracy: {(correct / total) * 100}%, Precision: {precision}, Recall: {recall}, F1 Score: {f1}")

    print("Training complete.")

    # Save the trained model
    torch.save(model.state_dict(), "mlops74/models/trained_model.pth")

if __name__ == '__main__':
    train()