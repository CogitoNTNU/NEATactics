import torch
import platform
import warnings
import pytest

@pytest.mark.environment
def test_cuda():
    if not torch.cuda.is_available():
        warnings.warn("You do not have CUDA enabled on your machine, large tensor operations will be slow")

@pytest.mark.environment
def test_os():
    if platform.system() == "Windows":
        warnings.warn("You might encounter issues with gym-super-mario-bros on Windows")
