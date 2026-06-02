---
audio: false
generated: true
lang: en
layout: post
title: Stable Diffusion Proxy Issue
translated: false
type: note
---

Based on the error and your environment, here's how to fix the "Unknown scheme for proxy URL" issue:

### Solution:
The error occurs because **`httpx` doesn't support `socks://` proxies by default**. You have two options:

#### Option 1: Remove the SOCKS Proxy Reference
1. Check your environment variables for stray proxy settings:
   ```bash
   env | grep -i proxy
   ```
   Look for `socks://` references (especially `ALL_PROXY` or `http_proxy`).

2. Unset the problematic variable (replace `VAR_NAME` with the actual name found above):
   ```bash
   unset VAR_NAME  # e.g., unset ALL_PROXY
   ```

#### Option 2: Add SOCKS Support to `httpx`
1. Activate your Python virtual environment:
   ```bash
   source /home/lzw/Projects/stable-diffusion-webui/venv/bin/activate
   ```

2. Install required dependencies:
   ```bash
   pip install -U "httpx[socks]"
   ```

3. Deactivate the environment:
   ```bash
   deactivate
   ```

### Why this happens:
- Your main proxies (`HTTP_PROXY/HTTPS_PROXY`) use `http://` (supported), but something (likely another app/script) is setting a `socks://` proxy that `httpx` can't handle without extra packages.
- The stack trace shows Gradio/`httpx` is trying to use `socks://127.0.0.1:7891`, which isn't in your `checkproxy` output.

### Verification:
After fixing, run:
```bash
./webui.sh
```
The SOCKS proxy error should disappear.

> 💡 **Note**: If you didn't intentionally set a SOCKS proxy, investigate applications that might auto-configure proxies (e.g., VPNs, network managers, or shell config files like `~/.bashrc`).

---

The error `Torch is not able to use GPU; add --skip-torch-cuda-test to COMMANDLINE_ARGS variable to disable this check` indicates that PyTorch, used by Stable Diffusion WebUI, cannot detect or access a compatible GPU. This is likely because of missing CUDA libraries, an incompatible GPU, driver issues, or a configuration problem. Below are steps to fix this issue, tailored to your environment (glibc 2.35, Python 3.10.12, GCC 11.4.0, likely Ubuntu 22.04 based on glibc version).

### Steps to Fix the Issue

#### 1. **Verify GPU and CUDA Compatibility**
   - **Check if you have an NVIDIA GPU**:
     Run:
     ```bash
     lspci | grep -i nvidia
     ```
     This lists NVIDIA hardware. If no output appears, your system may not have an NVIDIA GPU, and PyTorch requires an NVIDIA GPU for CUDA support.
   - **Check NVIDIA driver installation**:
     Run:
     ```bash
     nvidia-smi
     ```
     If installed, this displays a table with GPU details (e.g., driver version, CUDA version). If not, install the NVIDIA driver:
     ```bash
     sudo apt-get update
     sudo apt-get install nvidia-driver-<version> nvidia-utils-<version> -y
     ```
     Replace `<version>` with the latest stable driver (e.g., `535` or `550`). Find the appropriate driver version with:
     ```bash
     ubuntu-drivers devices
     sudo ubuntu-drivers autoinstall
     ```
   - **Check CUDA version**:
     PyTorch requires CUDA libraries. Check the installed CUDA version:
     ```bash
     nvcc --version
     ```
     If not installed, install CUDA Toolkit:
     ```bash
     sudo apt-get install nvidia-cuda-toolkit -y
     ```
     Alternatively, download the latest CUDA Toolkit from NVIDIA's website (e.g., CUDA 11.8 or 12.1) and follow their installation guide.

#### 2. **Verify PyTorch Installation**
   The error suggests PyTorch is installed but cannot use the GPU. Ensure you have the correct PyTorch version with CUDA support.
   - **Check PyTorch installation**:
     Run:
     ```bash
     python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
     ```
     Expected output should include a PyTorch version (e.g., `2.0.1`) and `True` for `torch.cuda.is_available()`. If `False`, PyTorch is not detecting the GPU.
   - **Reinstall PyTorch with CUDA support**:
     For Python 3.10 and CUDA (e.g., 11.8), install PyTorch in your Stable Diffusion environment:
     ```bash
     cd /home/lzw/Projects/stable-diffusion-webui
     source venv/bin/activate
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```
     Replace `cu118` with your CUDA version (e.g., `cu121` for CUDA 12.1). Check supported versions at PyTorch's official site.
   - **Verify after reinstallation**:
     Run the check again:
     ```bash
     python3 -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
     ```

#### 3. **Bypass the CUDA Check (Temporary Workaround)**
   If you want to run Stable Diffusion without GPU support (e.g., for testing on CPU), bypass the CUDA check by adding `--skip-torch-cuda-test` to the command-line arguments.
   - Edit `webui-user.sh` (or create it if it doesn’t exist):
     ```bash
     nano /home/lzw/Projects/stable-diffusion-webui/webui-user.sh
     ```
     Add or modify the `COMMANDLINE_ARGS` line:
     ```bash
     export COMMANDLINE_ARGS="--skip-torch-cuda-test"
     ```
     Save and exit.
   - Run the script:
     ```bash
     ./webui.sh
     ```
     This allows Stable Diffusion to run on CPU, but performance will be significantly slower.

#### 4. **Ensure TCMalloc is Properly Configured**
   Your output shows TCMalloc (`libtcmalloc_minimal.so.4`) is detected and linked with `LD_PRELOAD`. Confirm it’s working:
   ```bash
   echo $LD_PRELOAD
   ```
   If it outputs `/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4`, you’re set. If not, set it manually:
   ```bash
   export LD_PRELOAD=/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4
   ```
   Or add it to `webui-user.sh`:
   ```bash
   export LD_PRELOAD=/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4
   ```

#### 5. **Check Environment Variables and Paths**
   Ensure your environment is correctly set up:
   - **Check LD_LIBRARY_PATH**:
     CUDA libraries must be accessible. Add them if needed:
     ```bash
     export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
     ```
     Add this to `~/.bashrc` or `webui-user.sh` for persistence.
   - **Activate virtual environment**:
     Always activate the Stable Diffusion virtual environment before running:
     ```bash
     cd /home/lzw/Projects/stable-diffusion-webui
     source venv/bin/activate
     ```

#### 6. **Update Stable Diffusion WebUI**
   Your version (`v1.10.1`, commit `82a973c`) may have compatibility issues. Update to the latest version:
   ```bash
   cd /home/lzw/Projects/stable-diffusion-webui
   git pull
   ```
   Then, reinstall dependencies:
   ```bash
   ./webui.sh
   ```

#### 7. **Troubleshooting**
   - **If `nvidia-smi` fails**: Reinstall the NVIDIA driver or check for GPU hardware issues.
   - **If PyTorch still doesn’t detect GPU**:
     - Ensure CUDA and cuDNN are installed correctly. Install cuDNN if missing:
       ```bash
       sudo apt-get install libcudnn8
       ```
     - Verify CUDA version compatibility with your GPU and PyTorch. For example, older GPUs (e.g., Kepler series) may not support CUDA 12.
   - **If errors persist**: Check the Stable Diffusion logs for detailed errors:
     ```bash
     cat /home/lzw/Projects/stable-diffusion-webui/log/webui.log
     ```
     Share any specific errors for further assistance.
   - **Hardware limitations**: If your GPU is too old (e.g., pre-2016 NVIDIA GPUs), it may not support modern CUDA versions. In this case, use `--skip-torch-cuda-test` or upgrade your GPU.

#### 8. **Run the Application**
   After applying the fixes, run the WebUI:
   ```bash
   cd /home/lzw/Projects/stable-diffusion-webui
   ./webui.sh
   ```
   If you fixed the GPU issue, the error should disappear. If using `--skip-torch-cuda-test`, it will run on CPU.

### Notes
- **System Info**: Your setup (glibc 2.35, Python 3.10.12, GCC 11.4.0) suggests Ubuntu 22.04, which is compatible with CUDA 11.8 or 12.1 and recent PyTorch versions.
- **Performance**: Running on CPU (with `--skip-torch-cuda-test`) is a fallback but will be slow. Fixing GPU support is recommended for Stable Diffusion.
- **TCMalloc**: The TCMalloc issue seems resolved based on your output. Ensure `LD_PRELOAD` remains set if you encounter memory-related issues.

If you still face issues or need help with specific error messages, please provide additional details (e.g., GPU model, CUDA version, or full logs), and I can refine the solution!
