import torch
import pytest
from smoke.models.model import MyNeuralNet # Run the tests from mlops74 directory

@pytest.fixture
def sample_input():
    # Generate a sample input tensor with the desired shape
    return torch.randn((1, 3, 224, 224))  # Shape should be (batch_size, channels, height, width)

def test_model_output_shape(sample_input):
    model = MyNeuralNet()
    output = model(sample_input)
    expected_shape = (1, 2)  # Binary classification model, so 2 output classes

    # Check if the output shape matches the expected shape
    assert output.shape == torch.Size(expected_shape), 'Output shape has to be (1, 2)'

def test_error_on_wrong_shape():
    model = MyNeuralNet()
    
    with pytest.raises(ValueError, match='Expected input as a 4D tensor!'):
        model(torch.randn(1, 2, 3))
