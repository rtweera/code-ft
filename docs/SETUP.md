# Setup Guide

Complete installation and environment setup instructions for the code-ft project.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Python Installation](#python-installation)
3. [Virtual Environment Setup](#virtual-environment-setup)
4. [Dependency Installation](#dependency-installation)
5. [GPU Setup](#gpu-setup)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS (12+), or Windows 10/11
- **Python**: 3.10 or higher
- **RAM**: 8GB (16GB recommended)
- **Disk Space**: 50GB minimum (100GB+ recommended for multiple models)

### GPU Setup (Recommended)
- **GPU**: NVIDIA GPU with CUDA compute capability 7.0+ (e.g., GTX 1070 or newer)
- **VRAM**: 6GB minimum (12GB+ recommended)
- **CUDA**: 11.8 or higher
- **cuDNN**: 8.6 or higher

### CPU-Only Setup
The project can run on CPU, but will be significantly slower:
- Training will take 10-100x longer
- Inference will be noticeably slower
- Suitable for small-scale experiments only

## Python Installation

### Linux (Ubuntu/Debian)

```bash
# Update package lists
sudo apt update
sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3.10 python3.10-venv python3.10-dev

# Verify installation
python3.10 --version
```

### macOS

```bash
# Using Homebrew
brew install python@3.10

# Verify installation
python3.10 --version
```

### Windows

1. Download Python 3.10+ from [python.org](https://www.python.org/downloads/)
2. Run the installer and **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

## Virtual Environment Setup

### Create Virtual Environment

```bash
# Navigate to project directory
cd code-ft

# Create virtual environment
python3.10 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Verify Activation

```bash
# You should see (venv) prefix in your terminal
which python  # Linux/macOS
# or
where python  # Windows
```

### Deactivate Virtual Environment

```bash
deactivate
```

## Dependency Installation

### Install Core Dependencies

```bash
# Ensure pip is up to date
pip install --upgrade pip setuptools wheel

# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### Install PyTorch (CUDA support)

```bash
# For CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# For CPU only
pip install torch torchvision torchaudio
```

### Install Transformers and PEFT

```bash
# Install Hugging Face libraries for model handling
pip install transformers peft datasets accelerate
```

## GPU Setup

### NVIDIA CUDA Installation

#### Ubuntu/Debian

```bash
# Add NVIDIA repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl https://repo.download.nvidia.com/XLA-TF/ubuntu2204/nvidia-docker.gpg | sudo apt-key add -

# Install CUDA toolkit
sudo apt update
sudo apt install nvidia-cuda-toolkit nvidia-utils

# Verify installation
nvidia-smi
nvcc --version
```

#### macOS

Not directly supported. Use Docker or cloud GPU providers.

#### Windows

1. Download CUDA Toolkit from [nvidia.com](https://developer.nvidia.com/cuda-downloads)
2. Run installer and follow prompts
3. Add to PATH:
   ```
   C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin
   C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvml.dll
   ```
4. Verify:
   ```bash
   nvidia-smi
   ```

### GPU Memory Optimization

For limited VRAM:

```bash
# Enable mixed precision training (in your training script)
from torch.cuda.amp import autocast, GradScaler

# Use gradient checkpointing
model.gradient_checkpointing_enable()

# Reduce batch size
batch_size = 4  # Start small, increase if VRAM allows
```

## Verification

### Verify Python and Pip

```bash
python --version  # Should show 3.10+
pip --version
```

### Verify Key Packages

```bash
python -c "import torch; print(f'PyTorch {torch.__version__}')"
python -c "import transformers; print(f'Transformers {transformers.__version__}')"
python -c "import peft; print(f'PEFT installed')"
python -c "import pandas; print(f'Pandas {pandas.__version__}')"
```

### Test GPU Access (if applicable)

```bash
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

### Test Data Processing

```bash
cd data-processing
python -c "from format_dataset import DatasetFormatter; print('DatasetFormatter imported successfully')"
```

## Troubleshooting

### Common Issues and Solutions

#### Issue: `ModuleNotFoundError: No module named 'torch'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS

# Reinstall PyTorch
pip install torch --force-reinstall
```

#### Issue: `CUDA out of memory` during training

**Solutions:**
1. Reduce batch size:
   ```python
   training_args.per_device_train_batch_size = 2
   ```

2. Enable gradient accumulation:
   ```python
   training_args.gradient_accumulation_steps = 4
   ```

3. Use 8-bit quantization:
   ```bash
   pip install bitsandbytes
   ```

#### Issue: `nvidia-smi` command not found

**Solutions:**
1. Check CUDA installation:
   ```bash
   ls /usr/local/cuda  # Linux
   ```

2. Add to PATH:
   ```bash
   export PATH=/usr/local/cuda/bin:$PATH
   export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
   ```

3. Reinstall CUDA toolkit

#### Issue: Python version mismatch

**Solution:**
```bash
# Use specific Python version
python3.10 -m venv venv
source venv/bin/activate
```

#### Issue: Permission denied when installing packages

**Solution:**
```bash
# Use --user flag or virtual environment (recommended)
pip install --user -r requirements.txt

# Or create new virtual environment with correct permissions
python3.10 -m venv venv --clear
source venv/bin/activate
pip install -r requirements.txt
```

### Debug Information

Collect debug information for issues:

```bash
# Python version
python --version

# Installed packages
pip list

# GPU information
nvidia-smi

# PyTorch configuration
python -c "import torch; print(torch.cuda.get_device_properties(0))"

# System information
uname -a  # Linux/macOS
systeminfo  # Windows
```

## Next Steps

Once setup is complete:

1. **Configure Data**: Set up your Ballerina code dataset
2. **Prepare Environment**: Review [ARCHITECTURE.md](ARCHITECTURE.md)
3. **Process Data**: Follow [DATA_PROCESSING.md](DATA_PROCESSING.md)
4. **Start Training**: See [TRAINING.md](TRAINING.md)
5. **Deploy Model**: Check [INFERENCE.md](INFERENCE.md)

---

For issues or questions, see [FAQ.md](FAQ.md) or open an issue on GitHub.
