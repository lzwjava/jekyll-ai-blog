#!/usr/bin/env python3
"""
System Information Script for Ubuntu Server
Collects and displays system information including OS, architecture, Python, Java, etc.
"""

import platform
import subprocess
import os
import sys
import json


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


def get_os_info():
    """Get OS distribution and version."""
    # Try /etc/os-release first (modern method)
    os_info = {}
    try:
        with open("/etc/os-release", "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"')
                    os_info[key.lower()] = value
    except (FileNotFoundError, PermissionError):
        pass

    if "pretty_name" in os_info:
        os_name = os_info["pretty_name"]
    elif "name" in os_info:
        os_name = os_info["name"]
        if "version" in os_info:
            os_name += f" {os_info['version']}"
    else:
        # Fallback to lsb_release
        os_name = run_command("lsb_release -d -s")
        if not os_name:
            os_name = "Unknown"

    return os_name


def get_architecture():
    """Get system architecture."""
    machine = platform.machine().lower()
    if machine in ["x86_64", "amd64"]:
        return "64-bit"
    elif machine in ["i386", "i686"]:
        return "32-bit"
    else:
        return f"{machine} ({'64-bit' if sys.maxsize > 2**32 else '32-bit'})"


def get_python_version():
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_java_version():
    """Get Java version."""
    # Try multiple common java commands
    for java_cmd in ["java", "java8", "java11", "java17", "java21"]:
        version = run_command(f"{java_cmd} -version 2>&1 | head -n 1")
        if version and ("java" in version.lower() or "openjdk" in version.lower()):
            # Extract version number
            if '"' in version:
                return version.split('"')[1]
            return version.split()[2] if len(version.split()) > 2 else version
    return "Java not found"


def get_gnome_version():
    """Get Gnome version if available."""
    # Check for Gnome session
    gnome_session = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "gnome" in gnome_session:
        # Try to get gnome-shell version
        version = run_command("gnome-shell --version 2>&1")
        if version:
            return version.split()[-1] if len(version.split()) > 1 else version

    # Check if gnome is installed but not running
    if run_command("which gnome-shell") or run_command("which gdm"):
        return "GNOME installed (not currently running)"

    return "GNOME not detected"


def get_kernel_info():
    """Get kernel version."""
    return run_command("uname -r")


def get_disk_info():
    """Get disk usage information."""
    try:
        result = subprocess.run(
            "df -h /", shell=True, capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                # Get the root filesystem line
                root_line = lines[1]
                parts = root_line.split()
                if len(parts) >= 6:
                    total = parts[1]
                    used = parts[2]
                    available = parts[3]
                    use_percent = parts[4]
                    mount = parts[5]
                    return f"Total: {total}, Used: {used} ({use_percent}), Available: {available} (mounted on {mount})"
    except (subprocess.SubprocessError, subprocess.TimeoutExpired):
        pass
    return "Unable to retrieve disk information"


def get_memory_info():
    """Get memory and RAM information."""
    try:
        with open("/proc/meminfo", "r") as f:
            mem_info = f.read()

        total_kb = 0
        available_kb = 0

        for line in mem_info.split("\n"):
            if line.startswith("MemTotal:"):
                total_kb = int(line.split()[1])
            elif line.startswith("MemAvailable:"):
                available_kb = int(line.split()[1])

        if total_kb and available_kb:
            total_gb = total_kb / 1024 / 1024
            available_gb = available_kb / 1024 / 1024
            used_gb = total_gb - available_gb
            used_percent = (used_gb / total_gb) * 100

            return f"Total: {total_gb:.1f} GB, Used: {used_gb:.1f} GB ({used_percent:.1f}%), Available: {available_gb:.1f} GB"
    except (FileNotFoundError, PermissionError, ValueError):
        pass
    return "Unable to retrieve memory information"


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


def main():
    """Main function to collect and display system information."""
    print("=== Ubuntu Server System Information ===")
    print()

    # OS Information
    os_name = get_os_info()
    architecture = get_architecture()

    print("Operating System Information:")
    print(f"  Distribution: {os_name}")
    print(f"  Architecture: {architecture}")

    kernel = get_kernel_info()
    if kernel:
        print(f"  Kernel: {kernel}")

    print()

    # Programming Languages
    print("Programming Languages:")
    python_version = get_python_version()
    print(f"  Python: {python_version}")

    java_version = get_java_version()
    print(f"  Java: {java_version}")
    print()

    # Desktop Environment
    gnome_info = get_gnome_version()
    print("Desktop Environment:")
    print(f"  GNOME: {gnome_info}")
    print()

    # Additional system info
    print("System Details:")
    print(f"  Platform: {platform.platform()}")
    print(f"  Processor: {platform.processor() or 'Unknown'}")

    # Hardware information
    memory_info = get_memory_info()
    print(f"  Memory: {memory_info}")

    disk_info = get_disk_info()
    print(f"  Disk: {disk_info}")
    print()

    # GPU and CUDA information
    print("Graphics and Compute:")
    gpu_info = get_gpu_info()
    gpu_lines = gpu_info.split("\n")
    for line in gpu_lines:
        print(f"  {line}")

    cuda_info = get_cuda_info()
    cuda_lines = cuda_info.split("\n")
    for line in cuda_lines:
        print(f"  {line}")
    print()


if __name__ == "__main__":
    main()
