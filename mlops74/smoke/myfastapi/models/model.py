import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F

class MyNeuralNet(nn.Module):
    def __init__(self, num_classes=2, dropout_rate=0.5) -> None:
        super(MyNeuralNet, self).__init__()
        resnet = models.resnet34(pretrained=True)
        self.features = nn.Sequential(*list(resnet.children())[:-2])
        self.avgpool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(resnet.fc.in_features, num_classes)
        self.dropout = nn.Dropout(p=dropout_rate)
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim != 4:
            raise ValueError('Expected input as a 4D tensor!')
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = self.fc(x)
        return torch.sigmoid(x)  # Use torch.sigmoid instead of F.sigmoid

#not needed after initial creation of model_scripted -> causes multiple copies for some reason when something else call this...

#model = MyNeuralNet()

#print(model)

# Script the model using jit
#scripted_model = torch.jit.script(model)

# Save the scripted model with the correct method
#torch.jit.save(scripted_model, "model_scripted.pt")