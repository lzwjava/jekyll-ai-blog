"""
Intel oneAPI GPU Computing Examples for Python
Demonstrates various ways to use Intel GPU acceleration
"""

# ============================================
# Example 1: Intel Extension for PyTorch
# ============================================
import torch
import intel_extension_for_pytorch as ipex


def pytorch_gpu_example():
    """Use Intel GPU with PyTorch"""
    print("=== PyTorch with Intel GPU ===")

    # Check if XPU (Intel GPU) is available
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        device = torch.device("xpu")
        print(f"Intel GPU available: {torch.xpu.get_device_name(0)}")
    else:
        device = torch.device("cpu")
        print("Intel GPU not available, using CPU")

    # Create tensors on Intel GPU
    x = torch.randn(1000, 1000).to(device)
    y = torch.randn(1000, 1000).to(device)

    # Perform computation on GPU
    z = torch.matmul(x, y)

    print(f"Matrix multiplication result shape: {z.shape}")
    print(f"Result device: {z.device}")

    return z


# ============================================
# Example 2: NumPy with dpctl (Data Parallel Control)
# ============================================
try:
    import dpctl
    import dpctl.tensor as dpt

    def dpctl_example():
        """Use Intel GPU with dpctl"""
        print("\n=== dpctl GPU Computing ===")

        # List available devices
        print("Available devices:")
        for i, device in enumerate(dpctl.get_devices()):
            print(f"  {i}: {device.name} ({device.device_type})")

        # Try to get GPU device
        try:
            gpu_queue = dpctl.SyclQueue("gpu")
            print(f"Using GPU: {gpu_queue.sycl_device.name}")
        except:
            gpu_queue = dpctl.SyclQueue("cpu")
            print("GPU not available, using CPU")

        # Create arrays on device
        x = dpt.arange(1000000, device=gpu_queue.sycl_device)
        y = dpt.arange(1000000, device=gpu_queue.sycl_device)

        # Perform computation
        z = x + y

        print(f"Array computation completed on: {z.device}")
        print(f"Result sum: {dpt.sum(z)}")

        return z

except ImportError:

    def dpctl_example():
        print("\n=== dpctl not installed ===")
        print("Install with: pip install dpctl")


# ============================================
# Example 3: Intel Extension for Scikit-learn
# ============================================
try:
    from sklearnex import patch_sklearn

    patch_sklearn()

    from sklearn.cluster import KMeans
    import numpy as np

    def sklearn_gpu_example():
        """Use Intel GPU acceleration for scikit-learn"""
        print("\n=== Scikit-learn with Intel GPU Acceleration ===")

        # Generate sample data
        X = np.random.rand(10000, 50)

        # KMeans will automatically use Intel optimizations
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans.fit(X)

        print("KMeans clustering completed")
        print(f"Cluster centers shape: {kmeans.cluster_centers_.shape}")

        return kmeans

except ImportError:

    def sklearn_gpu_example():
        print("\n=== scikit-learn-intelex not installed ===")
        print("Install with: pip install scikit-learn-intelex")


# ============================================
# Example 4: Check System Info
# ============================================
def check_intel_gpu():
    """Check Intel GPU availability and info"""
    print("\n=== Intel GPU System Check ===")

    # Check PyTorch XPU
    try:
        import torch

        if hasattr(torch, "xpu") and torch.xpu.is_available():
            print("✓ PyTorch XPU available")
            print(f"  Device count: {torch.xpu.device_count()}")
            print(f"  Device name: {torch.xpu.get_device_name(0)}")
        else:
            print("✗ PyTorch XPU not available")
    except Exception as e:
        print(f"✗ PyTorch check failed: {e}")

    # Check dpctl
    try:
        import dpctl

        devices = dpctl.get_devices()
        gpu_devices = [d for d in devices if d.is_gpu]
        if gpu_devices:
            print(f"✓ dpctl found {len(gpu_devices)} GPU(s)")
            for gpu in gpu_devices:
                print(f"  - {gpu.name}")
        else:
            print("✗ No GPUs found via dpctl")
    except Exception as e:
        print(f"✗ dpctl check failed: {e}")


# ============================================
# Example 5: Simple Neural Network Training
# ============================================
def train_model_on_gpu():
    """Train a simple neural network on Intel GPU"""
    print("\n=== Training Neural Network on Intel GPU ===")

    import torch
    import torch.nn as nn

    # Determine device
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        device = torch.device("xpu")
        print("Training on Intel GPU")
    else:
        device = torch.device("cpu")
        print("Training on CPU")

    # Simple model
    model = nn.Sequential(nn.Linear(10, 50), nn.ReLU(), nn.Linear(50, 1)).to(device)

    # Optimize with IPEX
    model = ipex.optimize(model)

    # Training data
    X = torch.randn(1000, 10).to(device)
    y = torch.randn(1000, 1).to(device)

    # Training loop
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()

    for epoch in range(10):
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()

        if epoch % 2 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    print("Training completed!")


# ============================================
# Main execution
# ============================================
if __name__ == "__main__":
    print("Intel GPU Computing Examples\n")

    # Run system check first
    check_intel_gpu()

    # Run examples
    try:
        pytorch_gpu_example()
    except Exception as e:
        print(f"PyTorch example failed: {e}")

    try:
        dpctl_example()
    except Exception as e:
        print(f"dpctl example failed: {e}")

    try:
        sklearn_gpu_example()
    except Exception as e:
        print(f"Sklearn example failed: {e}")

    try:
        train_model_on_gpu()
    except Exception as e:
        print(f"Training example failed: {e}")

    print("\n=== All examples completed ===")
