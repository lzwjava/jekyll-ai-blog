#!/usr/bin/env python3
"""
GPU Information Script for Linux Systems
Collects and displays GPU information including NVIDIA, AMD, Intel GPUs and CUDA details.
"""

import subprocess
import sys


def run_command(cmd, fallback=None):
    """Run a command and return its output, or fallback if it fails."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return fallback
    except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
        return fallback


def get_gpu_info():
    """Get GPU information."""
    gpu_info = []

    # Try NVIDIA GPUs first
    nvidia_cmd = run_command(
        "nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free --format=csv,noheader,nounits"
    )
    if nvidia_cmd and "failed" not in nvidia_cmd.lower():
        lines = nvidia_cmd.strip().split("\n")
        for i, line in enumerate(lines):
            parts = [part.strip().strip('"') for part in line.split(",")]
            if len(parts) >= 4:
                name = parts[0]
                total_mb = parts[1]
                used_mb = parts[2]
                free_mb = parts[3]
                gpu_info.append(
                    f"NVIDIA {name}: {total_mb} MB total, {used_mb} MB used, {free_mb} MB free"
                )

    # Try AMD GPUs
    amd_cmd = run_command(
        r"lspci -v | grep -i 'vga.*amd\|vga.*ati\|3d.*amd\|3d.*ati' | head -5"
    )
    if amd_cmd:
        gpu_info.append(f"AMD GPU detected: {amd_cmd}")

    # Try Intel GPUs
    intel_cmd = run_command("lspci -v | grep -i 'vga.*intel' | head -5")
    if intel_cmd:
        gpu_info.append(f"Intel GPU detected: {intel_cmd}")

    # General PCI GPUs as fallback
    pci_cmd = run_command("lspci | grep -i vga | head -5")
    if pci_cmd and not gpu_info:
        gpu_info.append(f"GPU detected: {pci_cmd}")

    if gpu_info:
        return "\n".join(gpu_info)
    else:
        return "No GPU detected"


def get_cuda_info():
    """Get CUDA and NVIDIA driver information."""
    cuda_versions = []

    # Check NVIDIA driver
    driver_version = run_command(
        "nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits"
    )
    if driver_version and "failed" not in driver_version.lower():
        cuda_versions.append(f"NVIDIA Driver: {driver_version}")

    # Check CUDA runtime version
    cuda_version = run_command(
        "nvidia-smi --query-gpu=cuda_runtime_version --format=csv,noheader,nounits"
    )
    if cuda_version and "failed" not in cuda_version.lower():
        cuda_versions.append(f"CUDA Runtime: {cuda_version}")

    # Check nvcc compiler version
    nvcc_version = run_command(
        "nvcc --version | grep -i 'release' | awk '{print $6}' | cut -d',' -f1"
    )
    if nvcc_version and nvcc_version != "":
        cuda_versions.append(f"NVCC Compiler: {nvcc_version}")

    # Check cuDNN version (common location)
    cudnn_version = run_command(
        "cat /usr/include/cudnn_version.h 2>/dev/null | grep -w CUDNN_MAJOR | awk '{print $3}' | tr -d ';' | xargs"
    )
    if cudnn_version:
        cudnn_minor = run_command(
            "cat /usr/include/cudnn_version.h 2>/dev/null | grep -w CUDNN_MINOR | awk '{print $3}' | tr -d ';'"
        )
        cudnn_patch = run_command(
            "cat /usr/include/cudnn_version.h 2>/dev/null | grep -w CUDNN_PATCHLEVEL | awk '{print $3}' | tr -d ';'"
        )
        full_cudnn = f"{cudnn_version}.{cudnn_minor}.{cudnn_patch}"
        cuda_versions.append(f"cuDNN: {full_cudnn}")

    if cuda_versions:
        return "\n".join(cuda_versions)
    else:
        return "CUDA/NVIDIA drivers not detected"


def get_vulkan_info():
    """Get Vulkan information if available."""
    vulkan_info = []

    # Check Vulkan ICD (Installable Client Driver)
    vulkan_icd = run_command(
        "vulkaninfo --summary 2>/dev/null | grep -i 'device name' | head -3"
    )
    if vulkan_icd:
        vulkan_info.append(f"Vulkan ICD: {vulkan_icd}")

    # Check Vulkan SDK version
    vulkan_sdk = run_command(
        "vulkaninfo --summary 2>/dev/null | grep -i 'vulkan' | head -1"
    )
    if vulkan_sdk:
        vulkan_info.append(f"Vulkan SDK: {vulkan_sdk}")

    if vulkan_info:
        return "\n".join(vulkan_info)
    else:
        return "Vulkan not detected"


def check_proxy_settings():
    """Check for proxy settings that might affect GPU operations."""
    import os

    proxies = []
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")

    if http_proxy or https_proxy:
        if http_proxy:
            proxies.append(f"HTTP_PROXY: {http_proxy}")
        if https_proxy:
            proxies.append(f"HTTPS_PROXY: {https_proxy}")
        return "🚀 **Proxy Settings Detected:**\n   - " + "\n   - ".join(proxies)
    return None


def main():
    """Main function to collect and display GPU information."""
    proxy_info = check_proxy_settings()
    if proxy_info:
        print(proxy_info)
        print()

    print("=== GPU System Information ===")
    print()

    # GPU Information
    print("GPU Information:")
    gpu_info = get_gpu_info()
    if gpu_info.startswith("No GPU"):
        print(f"  {gpu_info}")
    else:
        # Indent multi-line output
        for line in gpu_info.split("\n"):
            print(f"  {line}")
    print()

    # CUDA/NVIDIA Information
    cuda_info = get_cuda_info()
    if cuda_info != "CUDA/NVIDIA drivers not detected":
        print("CUDA/NVIDIA Information:")
        for line in cuda_info.split("\n"):
            print(f"  {line}")
        print()

    # Vulkan Information
    vulkan_info = get_vulkan_info()
    if vulkan_info != "Vulkan not detected":
        print("Vulkan Information:")
        for line in vulkan_info.split("\n"):
            print(f"  {line}")
        print()


if __name__ == "__main__":
    main()
