import torch
import pytest
from mlops74.smoke.models.model import MyNeuralNet

@pytest.fixture
def sample_input():
    # Generate a sample input tensor with the desired shape
    return torch.randn((1, 3, 224, 224))  # Shape should be (batch_size, channels, height, width)

def test_model_output_shape(sample_input):
    model = MyNeuralNet()
    output = model(sample_input)
    expected_shape = (1, 2)  # Binary classification model, so 2 output classes

    # Check if the output shape matches the expected shape
    assert output.shape == torch.Size(expected_shape)
