---
audio: false
generated: true
lang: en
layout: post
title: Fix the TCMalloc Error
translated: false
type: note
---

The error "Cannot locate TCMalloc. Do you have tcmalloc or google-perftool installed on your system? (improves CPU memory usage)" indicates that the TCMalloc library, part of Google's gperftools, is not installed or not properly configured on your Linux system. TCMalloc is a memory allocator that can improve performance and reduce memory usage, particularly in applications like Stable Diffusion. Here's how to fix this issue:

### Steps to Fix the TCMalloc Error

1. **Install TCMalloc and Google Perftools**
   Depending on your Linux distribution, use the appropriate package manager to install the required libraries.

   - **For Ubuntu/Debian-based systems**:
     ```bash
     sudo apt-get update
     sudo apt-get install libgoogle-perftools-dev libtcmalloc-minimal4 -y
     ```
     This installs both the full `libgoogle-perftools-dev` (includes TCMalloc) and `libtcmalloc-minimal4` (a lightweight version).[](https://blog.csdn.net/yang553566463/article/details/132167437)[](https://sakari.niittymaa.com/blog_install-automatic1111-using-wsl)

   - **For Fedora-based systems**:
     ```bash
     sudo dnf install gperftools-libs -y
     ```
     This installs the necessary TCMalloc libraries.[](https://docs.suricata.io/en/latest/performance/tcmalloc.html)

   - **For CentOS/RHEL-based systems**:
     ```bash
     sudo yum install gperftools-libs -y
     ```
     If the package is not available in the default repositories, you may need to enable the EPEL repository first:
     ```bash
     sudo yum install epel-release
     sudo yum install gperftools-libs -y
     ```

2. **Verify Installation**
   After installation, check if TCMalloc is installed:
   ```bash
   dpkg -l | grep tcmalloc
   ```
   You should see `libtcmalloc-minimal4` or similar packages listed. Alternatively, check the library path:
   ```bash
   dpkg -L libgoogle-perftools-dev | grep libtcmalloc.so
   ```
   This will show the path to the TCMalloc library (e.g., `/usr/lib/libtcmalloc.so.4`).[](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/6722)

3. **Set the LD_PRELOAD Environment Variable**
   To ensure your application uses TCMalloc, set the `LD_PRELOAD` environment variable to point to the TCMalloc library. This can be done temporarily or permanently.

   - **Temporarily (for the current session)**:
     Run your application with `LD_PRELOAD` set:
     ```bash
     export LD_PRELOAD=/usr/lib/libtcmalloc.so.4
     ./launch.py
     ```
     Replace `/usr/lib/libtcmalloc.so.4` with the actual path found in step 2 if different.[](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/6722)

   - **Permanently (for Stable Diffusion or similar)**:
     If you're using a script like `webui.sh` (common with Stable Diffusion), edit the script (e.g., `webui-user.sh`) to include:
     ```bash
     export LD_PRELOAD=libtcmalloc.so.4
     ```
     Save the file and rerun the script:
     ```bash
     ./webui.sh
     ```
     Alternatively, add it to your shell configuration (e.g., `~/.bashrc` or `~/.zshrc`):
     ```bash
     echo 'export LD_PRELOAD=/usr/lib/libtcmalloc.so.4' >> ~/.bashrc
     source ~/.bashrc
     ```

4. **Re-run the Application**
   After installing TCMalloc and setting `LD_PRELOAD`, restart your application:
   ```bash
   ./launch.py
   ```
   The error should no longer appear, and you may notice improved memory usage or performance.[](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/6722)

5. **Troubleshooting**
   - **If the library path is incorrect**: If `LD_PRELOAD` fails (e.g., "cannot open shared object file"), verify the exact library name and path:
     ```bash
     find /usr/lib -name "libtcmalloc*.so*"
     ```
     Update `LD_PRELOAD` with the correct path (e.g., `libtcmalloc_minimal.so.4` if using the minimal version).
   - **If the error persists**: Ensure the installed TCMalloc version is compatible with your system (glibc 2.35 and GCC 11.4.0 in your case). If issues continue, try installing from source:
     ```bash
     git clone https://github.com/google/tcmalloc.git
     cd tcmalloc
     bazel build //tcmalloc:hello_main
     bazel run //tcmalloc:hello_main
     ```
     Follow the TCMalloc Quickstart guide for detailed instructions.[](https://google.github.io/tcmalloc/quickstart.html)
   - **Memory issues**: If you encounter allocation failures or crashes, ensure your system has sufficient memory and that TCMalloc is not conflicting with other allocators.[](https://stackoverflow.com/questions/tagged/tcmalloc)

6. **Optional: Verify TCMalloc Usage**
   To confirm TCMalloc is working, you can run a simple test program or check memory usage with tools like `top` or `htop` while your application runs. TCMalloc typically reduces memory fragmentation and may provide a slight performance boost.[](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/6722)

### Additional Notes
- **Why TCMalloc?** TCMalloc is a high-performance memory allocator that reduces CPU memory usage and fragmentation, especially in threaded applications like Stable Diffusion. It’s not strictly required but can improve performance.[](https://docs.suricata.io/en/latest/performance/tcmalloc.html)[](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/6722)
- **Compatibility**: Your system (glibc 2.35, Python 3.10.12, GCC 11.4.0) is compatible with the latest TCMalloc versions, so the above steps should work. If you’re using a custom-built application, ensure it’s compiled with TCMalloc support.[](https://stackoverflow.com/questions/29205141/how-to-use-tcmalloc)
- **Stable Diffusion Context**: This error often appears with AUTOMATIC1111’s Stable Diffusion WebUI. The above steps, particularly installing `libgoogle-perftools-dev` and setting `LD_PRELOAD`, are known to resolve it.[](https://github.com/AUTOMATIC1111/stable-diffusion-webui/issues/10117)[](https://github.com/AUTOMATIC1111/stable-diffusion-webui/discussions/6722)[](https://blog.csdn.net/yang553566463/article/details/132167437)

If you encounter specific errors or need help with a particular Linux distribution, let me know, and I can tailor the instructions further!
