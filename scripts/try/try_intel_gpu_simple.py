import torch
import intel_extension_for_pytorch as ipex

print(f"PyTorch version: {torch.__version__}")
print(f"IPEX version: {ipex.__version__}")

if hasattr(torch, "xpu") and torch.xpu.is_available():
    print(f"✓ Intel GPU available: {torch.xpu.get_device_name(0)}")

    # Simple computation
    x = torch.randn(100, 100, device="xpu")
    y = torch.randn(100, 100, device="xpu")
    z = x @ y
    print("✓ Successfully computed on GPU")
else:
    print("✗ Intel GPU not detected")
