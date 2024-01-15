import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

class MyNeuralNet(nn.Module):
    def __init__(self, num_classes=2, dropout_rate=0.5) -> None:
        super(MyNeuralNet, self).__init__()
        resnet = models.resnet34(pretrained=True)  # We can choose from ResNet variants (18,34,50,101,110,152..) if needed
        self.features = nn.Sequential(*list(resnet.children())[:-2])  # Remove the last two layers (avgpool and fc) in case we want to add something more
        
        self.avgpool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(resnet.fc.in_features, num_classes)
        self.dropout = nn.Dropout(p=dropout_rate)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = self.fc(x)
        return F.sigmoid(x)

#model = MyNeuralNet()

#print(model)
