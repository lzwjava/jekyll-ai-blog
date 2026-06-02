---
audio: false
generated: true
lang: zh
layout: post
title: Stable Diffusion代理问题
translated: true
type: note
---

根据错误信息和您的环境，以下是修复“Unknown scheme for proxy URL”问题的方法：

### 解决方案：
该错误出现是因为 **`httpx` 默认不支持 `socks://` 代理**。您有两个选择：

#### 方案一：移除 SOCKS 代理引用
1. 检查环境变量中是否有残留的代理设置：
   ```bash
   env | grep -i proxy
   ```
   查找 `socks://` 引用（特别是 `ALL_PROXY` 或 `http_proxy`）。

2. 取消设置有问题的变量（将 `VAR_NAME` 替换为上面找到的实际变量名）：
   ```bash
   unset VAR_NAME  # 例如：unset ALL_PROXY
   ```

#### 方案二：为 `httpx` 添加 SOCKS 支持
1. 激活您的 Python 虚拟环境：
   ```bash
   source /home/lzw/Projects/stable-diffusion-webui/venv/bin/activate
   ```

2. 安装所需依赖：
   ```bash
   pip install -U "httpx[socks]"
   ```

3. 退出虚拟环境：
   ```bash
   deactivate
   ```

### 问题原因：
- 您的主代理（`HTTP_PROXY/HTTPS_PROXY`）使用 `http://`（受支持），但某些程序（可能是其他应用/脚本）设置了 `socks://` 代理，而 `httpx` 在没有额外包的情况下无法处理。
- 堆栈跟踪显示 Gradio/`httpx` 正尝试使用 `socks://127.0.0.1:7891`，但该代理未在您的 `checkproxy` 输出中显示。

### 验证：
修复后运行：
```bash
./webui.sh
```
SOCKS 代理错误应该会消失。

> 💡 **注意**：如果您没有主动设置 SOCKS 代理，请检查可能自动配置代理的应用程序（例如 VPN、网络管理器或 shell 配置文件如 `~/.bashrc`）。

---

错误 `Torch is not able to use GPU; add --skip-torch-cuda-test to COMMANDLINE_ARGS variable to disable this check` 表明 Stable Diffusion WebUI 使用的 PyTorch 无法检测或访问兼容的 GPU。这可能是由于缺少 CUDA 库、GPU 不兼容、驱动问题或配置问题导致的。以下是针对您的环境（glibc 2.35、Python 3.10.12、GCC 11.4.0，根据 glibc 版本推测为 Ubuntu 22.04）的修复步骤。

### 问题解决步骤

#### 1. **验证 GPU 和 CUDA 兼容性**
   - **检查是否拥有 NVIDIA GPU**：
     运行：
     ```bash
     lspci | grep -i nvidia
     ```
     此命令将列出 NVIDIA 硬件。若无输出，则系统可能没有 NVIDIA GPU，而 PyTorch 需要 NVIDIA GPU 才能支持 CUDA。
   - **检查 NVIDIA 驱动安装**：
     运行：
     ```bash
     nvidia-smi
     ```
     若已安装，将显示包含 GPU 详细信息（如驱动版本、CUDA 版本）的表格。若未安装，请安装 NVIDIA 驱动：
     ```bash
     sudo apt-get update
     sudo apt-get install nvidia-driver-<version> nvidia-utils-<version> -y
     ```
     将 `<version>` 替换为最新的稳定驱动版本（例如 `535` 或 `550`）。可通过以下命令查找合适的驱动版本：
     ```bash
     ubuntu-drivers devices
     sudo ubuntu-drivers autoinstall
     ```
   - **检查 CUDA 版本**：
     PyTorch 需要 CUDA 库。检查已安装的 CUDA 版本：
     ```bash
     nvcc --version
     ```
     若未安装，请安装 CUDA Toolkit：
     ```bash
     sudo apt-get install nvidia-cuda-toolkit -y
     ```
     或者，从 NVIDIA 官网下载最新的 CUDA Toolkit（例如 CUDA 11.8 或 12.1）并按照其安装指南进行安装。

#### 2. **验证 PyTorch 安装**
   该错误表明 PyTorch 已安装但无法使用 GPU。请确保安装了正确版本且支持 CUDA 的 PyTorch。
   - **检查 PyTorch 安装**：
     运行：
     ```bash
     python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
     ```
     预期输出应包含 PyTorch 版本（例如 `2.0.1`）和 `torch.cuda.is_available()` 返回 `True`。若返回 `False`，则 PyTorch 未检测到 GPU。
   - **重新安装支持 CUDA 的 PyTorch**：
     针对 Python 3.10 和 CUDA（例如 11.8），在您的 Stable Diffusion 环境中安装 PyTorch：
     ```bash
     cd /home/lzw/Projects/stable-diffusion-webui
     source venv/bin/activate
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
     ```
     将 `cu118` 替换为您的 CUDA 版本（例如 CUDA 12.1 使用 `cu121`）。请在 PyTorch 官网查看支持的版本。
   - **重新安装后验证**：
     再次运行检查：
     ```bash
     python3 -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
     ```

#### 3. **绕过 CUDA 检查（临时解决方案）**
   如果希望在没有 GPU 支持的情况下运行 Stable Diffusion（例如在 CPU 上测试），可通过添加 `--skip-torch-cuda-test` 到命令行参数来绕过 CUDA 检查。
   - 编辑 `webui-user.sh`（若不存在则创建）：
     ```bash
     nano /home/lzw/Projects/stable-diffusion-webui/webui-user.sh
     ```
     添加或修改 `COMMANDLINE_ARGS` 行：
     ```bash
     export COMMANDLINE_ARGS="--skip-torch-cuda-test"
     ```
     保存并退出。
   - 运行脚本：
     ```bash
     ./webui.sh
     ```
     这将允许 Stable Diffusion 在 CPU 上运行，但性能会显著下降。

#### 4. **确保 TCMalloc 正确配置**
   您的输出显示已检测到 TCMalloc（`libtcmalloc_minimal.so.4`）并通过 `LD_PRELOAD` 链接。请确认其正常工作：
   ```bash
   echo $LD_PRELOAD
   ```
   若输出 `/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4`，则表示设置正确。否则，请手动设置：
   ```bash
   export LD_PRELOAD=/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4
   ```
   或将其添加到 `webui-user.sh`：
   ```bash
   export LD_PRELOAD=/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4
   ```

#### 5. **检查环境变量和路径**
   确保环境设置正确：
   - **检查 LD_LIBRARY_PATH**：
     CUDA 库必须可访问。如有需要，请添加：
     ```bash
     export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
     ```
     将此行添加到 `~/.bashrc` 或 `webui-user.sh` 以实现持久化。
   - **激活虚拟环境**：
     运行前务必激活 Stable Diffusion 虚拟环境：
     ```bash
     cd /home/lzw/Projects/stable-diffusion-webui
     source venv/bin/activate
     ```

#### 6. **更新 Stable Diffusion WebUI**
   您当前的版本（`v1.10.1`，提交 `82a973c`）可能存在兼容性问题。请更新至最新版本：
   ```bash
   cd /home/lzw/Projects/stable-diffusion-webui
   git pull
   ```
   然后重新安装依赖：
   ```bash
   ./webui.sh
   ```

#### 7. **故障排除**
   - **若 `nvidia-smi` 失败**：重新安装 NVIDIA 驱动或检查 GPU 硬件问题。
   - **若 PyTorch 仍无法检测 GPU**：
     - 确保 CUDA 和 cuDNN 已正确安装。若缺少 cuDNN，请安装：
       ```bash
       sudo apt-get install libcudnn8
       ```
     - 验证 CUDA 版本与您的 GPU 和 PyTorch 的兼容性。例如，较旧的 GPU（如 Kepler 系列）可能不支持 CUDA 12。
   - **若错误持续**：检查 Stable Diffusion 日志以获取详细错误信息：
     ```bash
     cat /home/lzw/Projects/stable-diffusion-webui/log/webui.log
     ```
     分享具体错误信息以获取进一步帮助。
   - **硬件限制**：如果您的 GPU 过于陈旧（例如 2016 年以前的 NVIDIA GPU），可能不支持现代 CUDA 版本。这种情况下，请使用 `--skip-torch-cuda-test` 或升级 GPU。

#### 8. **运行应用程序**
   应用修复后，运行 WebUI：
   ```bash
   cd /home/lzw/Projects/stable-diffusion-webui
   ./webui.sh
   ```
   若 GPU 问题已解决，错误将消失。若使用 `--skip-torch-cuda-test`，则将在 CPU 上运行。

### 注意事项
- **系统信息**：您的设置（glibc 2.35、Python 3.10.12、GCC 11.4.0）表明系统为 Ubuntu 22.04，该版本兼容 CUDA 11.8 或 12.1 以及近期版本的 PyTorch。
- **性能**：在 CPU 上运行（使用 `--skip-torch-cuda-test`）是备用方案，但速度较慢。建议修复 GPU 支持以正常运行 Stable Diffusion。
- **TCMalloc**：根据您的输出，TCMalloc 问题似乎已解决。若遇到内存相关问题，请确保 `LD_PRELOAD` 保持设置。

如果您仍然遇到问题或需要针对特定错误消息的帮助，请提供更多详细信息（例如 GPU 型号、CUDA 版本或完整日志），我将进一步优化解决方案！
