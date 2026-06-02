---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Enable Intel GPU Support for PyTorch
translated: false
type: note
---

Good progress! PyTorch and IPEX are now working together. However, your system doesn't have Intel GPU support enabled. Let me help you understand what's happening and how to fix it:

## Current Status

- ✓ PyTorch + IPEX installed correctly
- ✗ Intel GPU (XPU) support not available
- ✗ Missing optional packages (`dpctl`, `scikit-learn-intelex`)

## To Enable Intel GPU Support

### 1. **Check if you have an Intel GPU**

```bash
# Check your GPU hardware
lspci | grep -i vga
# or
lspci | grep -i display
```

### 2. **Install Intel GPU drivers** (if you have Intel Arc/Iris/UHD graphics)

For Ubuntu/Debian:

```bash
# Add Intel GPU repository
wget -qO - https://repositories.intel.com/gpu/intel-graphics.key | \
  sudo gpg --dearmor --output /usr/share/keyrings/intel-graphics.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/gpu/ubuntu jammy client" | \
  sudo tee /etc/apt/sources.list.d/intel-gpu-jammy.list

sudo apt update

# Install Level Zero and OpenCL runtimes
sudo apt install -y \
  intel-opencl-icd \
  intel-level-zero-gpu \
  level-zero \
  level-zero-dev
```

### 3. **Install additional Python packages**

```bash
# Install dpctl for Intel GPU device management
pip install dpctl

# Install scikit-learn with Intel optimizations
pip install scikit-learn-intelex
```

### 4. **Install PyTorch with XPU support**

```bash
# Uninstall CPU-only PyTorch
pip uninstall torch torchvision torchaudio

# Install PyTorch with Intel XPU support
pip install torch==2.8.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu

# Make sure IPEX matches
pip install intel-extension-for-pytorch==2.8.0
```

### 5. **Verify installation**

```bash
python -c "import torch; import intel_extension_for_pytorch as ipex; print('XPU available:', torch.xpu.is_available()); print('XPU device count:', torch.xpu.device_count() if torch.xpu.is_available() else 0)"
```

## About the Training Error

The error `"The optimizer should be given for training mode"` is a bug in your script. You need to pass an optimizer when training. Check your `try_intel_gpu.py` and ensure the training function includes an optimizer parameter.

**What Intel GPU hardware do you have?** Run `lspci | grep -i vga` to check, and I can give you more specific instructions.
