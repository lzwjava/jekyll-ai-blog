---
audio: false
generated: true
lang: en
layout: post
title: NVIDIA DKMS Build Issue
translated: false
type: note
---

It looks like you're encountering an error where the NVIDIA DKMS (Dynamic Kernel Module Support) module is failing to build for your new kernel, `6.8.0-60-generic`. This is a common issue when updating kernels, as the driver module needs to be recompiled for the new kernel version, and sometimes incompatibilities or build issues arise.

The key error messages are:
* `Building module(s)......(bad exit status: 2)`
* `Error! Bad return status for module build on kernel: 6.8.0-60-generic (x86_64)`
* `Consult /var/lib/dkms/nvidia/535.183.06/build/make.log for more information.`
* `dpkg: error processing package linux-image-6.8.0-60-generic (--configure):`
* `E: Sub-process /usr/bin/dpkg returned an error code (1)`

This means the NVIDIA driver version `535.183.06` could not be successfully compiled against kernel `6.8.0-60-generic`, which in turn has stopped the kernel image and related packages from being configured correctly.

Here's how you can try to fix this:

---

### 1. Examine the Build Log 🪵

The most crucial step is to check the detailed build log for specific error messages. This log will tell you *why* the compilation failed.
Open a terminal and run:
```bash
cat /var/lib/dkms/nvidia/535.183.06/build/make.log
```
Look for lines starting with `error:` or `fatal error:`. These will often point to missing files, compiler issues, or incompatibilities with the kernel source. The error `Applying patch disable_fstack-clash-protection_fcf-protection.patch... done.` followed by a build failure suggests the patch might not be fully compatible, or there are other issues the patch doesn't address.

---

### 2. Clean Up and Attempt to Fix Broken Packages 🛠️

First, you can try to let `apt` attempt to fix the broken dependencies and finish configuring packages.
```bash
sudo rm /var/crash/nvidia-dkms-535.0.crash # Remove old crash report to allow new ones
sudo apt --fix-broken install
sudo dpkg --configure -a
```
This might re-trigger the DKMS build. If it fails again, proceed to the next steps.

---

### 3. Ensure Kernel Headers are Correctly Installed 🧠

The DKMS build process requires the correct kernel headers for the kernel you're trying to build against.
```bash
sudo apt update
sudo apt install --reinstall linux-headers-6.8.0-60-generic linux-headers-generic-hwe-22.04
```
If you're not yet running the `6.8.0-60-generic` kernel (e.g., if the update was interrupted), you can specify the headers for your currently running kernel too, but the primary target here is `6.8.0-60-generic`.

---

### 4. Remove the Failing DKMS Module and Reconfigure ♻️

You can manually remove the problematic version of the NVIDIA module from DKMS and then try to let the system rebuild it.
```bash
sudo dkms remove nvidia/535.183.06 --all
```
Then, try to reconfigure the packages again:
```bash
sudo dpkg --configure -a
sudo apt update && sudo apt upgrade
```
This process should prompt DKMS to try and rebuild the module for the `6.8.0-60-generic` kernel.

---

### 5. Reinstall the NVIDIA Driver 💻

If the module still fails to build, the driver version `535.183.06` might have compatibility issues with kernel `6.8.0-60-generic`.

* **Purge the current problematic driver:**
    ```bash
    sudo apt-get purge nvidia-dkms-535 nvidia-driver-535
    sudo apt autoremove
    sudo apt clean
    ```

* **Install a suitable driver:**
    You can let Ubuntu try to install the recommended driver:
    ```bash
    sudo ubuntu-drivers autoinstall
    ```
    Alternatively, you can try to install the same version (if it's deemed compatible by the repositories now) or a potentially newer, more compatible version. For instance, to try installing the 535 series driver again:
    ```bash
    sudo apt update
    sudo apt install nvidia-driver-535
    ```
    (The package manager should pick the appropriate DKMS version.)

    After this, the system will attempt to build the DKMS module again.

---

### 6. Consider a Newer NVIDIA Driver Version 🚀

Kernel 6.8 is relatively new. It's possible that the NVIDIA 535 series driver has limitations with this kernel version. You might need a newer driver series (e.g., 545, 550, or newer, if available in your repositories or via NVIDIA's official channels/PPAs).

* Check available drivers:
    ```bash
    sudo apt search nvidia-driver
    ```
* If a newer proprietary driver is available (e.g., `nvidia-driver-550`), you could try installing that instead of `nvidia-driver-535`.
    ```bash
    sudo apt install nvidia-driver-VERSION_NUMBER # Replace VERSION_NUMBER
    ```

---

### 7. If You're Stuck in a Boot Loop or Have No GUI 📉

If the system fails to boot into a graphical environment:
* Boot into recovery mode or an older kernel (usually accessible from the GRUB menu during startup).
* Once in a command-line environment, you can try the steps above.
* If you need to temporarily use an open-source driver to get a GUI back while you fix the NVIDIA driver:
    ```bash
    sudo apt-get purge nvidia*
    sudo apt autoremove
    sudo apt install xserver-xorg-video-nouveau
    sudo reboot
    ```
    Then, attempt the NVIDIA driver installation again.

---

**Key takeaway:** The content of `/var/lib/dkms/nvidia/535.183.06/build/make.log` is very important. If the steps above don't work, the errors in that file will provide more specific clues, and you may need to search online for those specific errors in conjunction with your kernel version and NVIDIA driver version.

---

This output indicates a series of dependency and configuration problems in your Ubuntu system, likely related to kernel updates and the NVIDIA driver. Let's break down the issues and suggest potential solutions.

**Main Problems:**

1.  **Dependency Issues with `linux-generic-hwe-22.04`:**
    * It depends on `linux-headers-generic-hwe-22.04` with a specific version (`= 6.8.0-60.63~22.04.1`).
    * `linux-headers-generic-hwe-22.04` is not configured yet, causing the configuration of `linux-generic-hwe-22.04` to fail.

2.  **Failure to Configure `linux-image-6.8.0-60-generic`:**
    * The post-installation script for this kernel image failed with an exit status of 1.
    * The error log suggests this is related to the NVIDIA driver (`nvidia/535.183.06`) failing to build for this specific kernel version (`6.8.0-60-generic`).
    * The DKMS (Dynamic Kernel Module Support) build process for the NVIDIA driver failed. The log file `/var/lib/dkms/nvidia/535.183.06/build/make.log` will contain more details about the build error.
    * There's also an error related to creating a crash report for the NVIDIA DKMS failure, indicating a potential issue with the system's crash reporting mechanism or file system permissions.

3.  **Failure to Configure `linux-headers-6.8.0-60-generic` and `linux-headers-generic-hwe-22.04`:**
    * These likely failed because the `linux-image-6.8.0-60-generic` package configuration failed, which they might depend on.

**Potential Causes:**

* **Incomplete or interrupted kernel update:** The system might have been interrupted during a kernel upgrade, leaving some packages in an inconsistent state.
* **NVIDIA driver incompatibility:** The installed NVIDIA driver version (`535.183.06`) might have issues building against the new kernel version (`6.8.0-60-generic`).
* **DKMS issues:** There might be problems with the DKMS framework itself, preventing the NVIDIA driver from building.
* **File system issues:** The error about not being able to create a crash report might indicate a problem with disk space or file permissions in the `/var/crash/` directory.

**Troubleshooting Steps:**

1.  **Try to reconfigure the packages:**
    Open your terminal and run the following command:
    ```bash
    sudo dpkg --configure -a
    ```
    This command attempts to configure all packages that are in a half-configured state.

2.  **Check the NVIDIA DKMS build log:**
    Examine the log file for detailed error messages during the NVIDIA driver build:
    ```bash
    less /var/lib/dkms/nvidia/535.183.06/build/make.log
    ```
    This log might provide clues about missing dependencies or compilation errors.

3.  **Try to reinstall the NVIDIA driver:**
    You can try to remove and then reinstall the NVIDIA driver. First, try to purge it:
    ```bash
    sudo apt remove --purge nvidia-*
    sudo apt autoremove
    ```
    Then, try reinstalling it. You might want to try a different version if the current one is problematic:
    ```bash
    sudo apt install nvidia-driver-535  # Or a different recommended version
    ```
    After installation, reboot your system.

4.  **Clean the package cache and try again:**
    ```bash
    sudo apt clean
    sudo apt update
    sudo apt upgrade
    sudo dpkg --configure -a
    ```

5.  **Reinstall the problematic kernel and headers:**
    You can try to reinstall the specific kernel and header packages that are causing issues:
    ```bash
    sudo apt install --reinstall linux-image-6.8.0-60-generic linux-headers-6.8.0-60-generic linux-headers-generic-hwe-22.04 linux-generic-hwe-22.04
    ```
    After this, try configuring again:
    ```bash
    sudo dpkg --configure -a
    ```

6.  **Check disk space:**
    Ensure you have enough free space on your root partition (`/`) as this can sometimes cause issues during package installation and configuration.
    ```bash
    df -h /
    ```

7.  **Address the crash report error (if persistent):**
    If the error about `/var/crash/nvidia-dkms-535.0.crash` persists, you can try removing the file (if it exists and you don't need it for debugging) or checking the permissions of the `/var/crash/` directory.
    ```bash
    sudo rm -f /var/crash/nvidia-dkms-535.0.crash
    sudo chmod 777 /var/crash  # Be cautious with broad permissions, revert if unnecessary
    ```

8.  **Boot into a previous kernel:**
    If you have a previous kernel version installed, you can try booting into it from the GRUB menu. This can allow you to perform troubleshooting steps from a stable environment. If the system works with an older kernel, the issue is likely specific to the `6.8.0-60-generic` kernel or its interaction with the NVIDIA driver.

**Important Considerations:**

* **Backup:** Before making significant changes, especially involving package removal, it's always a good idea to have a backup of your important data.
* **Be patient:** Package configuration and installation can take some time.
* **Consult logs:** The error messages and log files (especially the NVIDIA DKMS build log) are crucial for diagnosing the exact cause of the problem.

Start with the first few steps and see if they resolve the issue. If not, proceed to the more involved solutions and carefully examine any error messages you encounter. Good luck!


---

This output from the NVIDIA DKMS build log indicates that the compilation is failing due to an **unrecognized command-line option: `-ftrivial-auto-var-init=zero`**.

This compiler option is a relatively recent addition to GCC (likely version 12 or later) and Clang. It seems that the compiler being used to build the NVIDIA driver for your kernel (6.8.0-60-generic) does not recognize this option.

**Possible Causes and Solutions:**

1.  **Outdated Compiler:** Your system might have an older version of GCC or Clang installed as the default compiler. The kernel headers might be compiled with a newer compiler that uses this option, but the NVIDIA driver build system is picking up an older one.

    **Solution:**
    * **Install a newer compiler:** You can try installing a more recent version of GCC.
        ```bash
        sudo apt update
        sudo apt install gcc-12  # Or a later version like gcc-13
        ```
    * **Update your build environment:** Ensure your build tools are up to date.
        ```bash
        sudo apt update
        sudo apt install build-essential
        ```
    * **Specify the compiler (if possible):** Some build systems allow you to specify the compiler to use. Check the NVIDIA driver build instructions or configuration files for options related to the compiler (e.g., `CC` environment variable).

2.  **Incompatibility with the Kernel Build Configuration:** The kernel you are using might have been built with a compiler that enabled this option, and the NVIDIA driver build system is inheriting or encountering it in a way that causes a failure with its own compiler.

    **Solution:**
    * **Try a different NVIDIA driver version:** The latest NVIDIA driver might have better compatibility with newer kernels and compiler features. You could try installing a more recent stable release.
        ```bash
        sudo apt update
        sudo apt install nvidia-driver-<latest-version>
        ```
        Replace `<latest-version>` with the newest recommended driver package name for your system. You can usually find this by searching `apt search nvidia-driver`.
    * **Downgrade your kernel (as a temporary workaround):** If you have a previous kernel version installed that worked with your NVIDIA driver, you can boot into that kernel from the GRUB menu. This isn't a permanent solution but can give you a working system while you troubleshoot the driver issue with the newer kernel.

3.  **Issue with the NVIDIA Driver Package:** There might be a problem with the specific NVIDIA driver package you are trying to install in relation to your kernel and compiler setup.

    **Solution:**
    * **Try a different installation method:** If you installed the driver via `apt`, you could try downloading the driver directly from the NVIDIA website and installing it using the `.run` file. Follow the instructions provided by NVIDIA carefully.
    * **Check for known issues:** Search online forums or the NVIDIA support website for known issues with the specific driver version and kernel combination you are using.

**Steps to Try:**

1.  **Check your GCC version:**
    ```bash
    gcc --version
    ```
    Compare this to the GCC version that might have been used to build the kernel (you might find information about the kernel build environment online for your Ubuntu version).

2.  **Try installing a newer NVIDIA driver:**
    ```bash
    sudo apt update
    sudo apt install nvidia-driver-550  # Example: try a newer version
    sudo reboot
    ```

3.  **If the above doesn't work, try purging and reinstalling the recommended driver:**
    ```bash
    sudo apt remove --purge nvidia-*
    sudo apt autoremove
    sudo apt update
    sudo ubuntu-drivers autoinstall  # Installs recommended drivers
    sudo reboot
    ```

4.  **If you still face issues, consider installing a newer GCC version (be cautious as this can sometimes have unintended side effects):**
    ```bash
    sudo apt install gcc-12 g++-12
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 12
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 12
    # You might want to keep the older version as well and switch back if needed
    # To switch back: sudo update-alternatives --config gcc and sudo update-alternatives --config g++
    sudo apt install build-essential # Ensure build tools are updated after compiler change
    sudo dpkg --configure -a # Reconfigure packages
    sudo reboot
    ```

Remember to reboot your system after trying any driver installation or significant system changes. Carefully monitor the output for any new error messages. If you continue to have problems, providing more details about your Ubuntu version might help in finding a more specific solution.

---

It looks like you're encountering dependency and DKMS (Dynamic Kernel Module Support) issues while trying to configure Linux kernel packages, particularly with the NVIDIA driver module failing to build for the new kernel (6.8.0-60-generic).

### Here's how to resolve this:

---

### **1. Fix Dependencies and Configure Packages**
First, try to fix the dependency issues and configure the packages:

```bash
sudo apt --fix-broken install
sudo dpkg --configure -a
```

If that doesn't work, manually force the configuration of the problematic packages:

```bash
sudo apt install -f linux-headers-generic-hwe-22.04 linux-generic-hwe-22.04
```

---

### **2. Reinstall NVIDIA Drivers**
The error shows that the NVIDIA DKMS module (`nvidia/535.183.06`) failed to build for kernel `6.8.0-60-generic`. To fix this:

#### **Option A: Reinstall the NVIDIA driver**
```bash
sudo apt install --reinstall nvidia-dkms-535 nvidia-driver-535
```

#### **Option B: Purge and Reinstall NVIDIA drivers**
If reinstalling doesn't work, try a clean reinstall:
```bash
sudo apt purge nvidia-*
sudo apt autoremove
sudo apt install nvidia-driver-535
```

#### **Option C: Temporarily boot into an older kernel**
If the system is unbootable, reboot into an older kernel (select it in GRUB) and then:
```bash
sudo apt remove linux-image-6.8.0-60-generic linux-headers-6.8.0-60-generic
sudo update-grub
```

---

### **3. Check DKMS Build Log**
The error mentions `/var/lib/dkms/nvidia/535.183.06/build/make.log`. Check it for details:
```bash
cat /var/lib/dkms/nvidia/535.183.06/build/make.log
```

This may reveal why the module failed to build (e.g., missing dependencies, compiler issues).

---

### **4. Manually Install Missing Dependencies**
If the log shows missing dependencies, install them:
```bash
sudo apt install build-essential linux-headers-generic
```

---

### **5. Rebuild DKMS Modules**
After fixing dependencies, manually rebuild the modules:
```bash
sudo dkms remove nvidia/535.183.06 --all
sudo dkms install nvidia/535.183.06
```

---

### **6. Update Initramfs**
After fixing the NVIDIA driver, update the initramfs:
```bash
sudo update-initramfs -u -k all
```

---

### **7. Final Fix Attempt**
If all else fails, remove the problematic kernel and stick with an older one:
```bash
sudo apt purge linux-image-6.8.0-60-generic linux-headers-6.8.0-60-generic
sudo apt autoremove
sudo update-grub
```

Then, wait for an updated NVIDIA driver or kernel before trying again.

---

### **8. Prevent Future Issues**
To avoid similar issues, consider:
- **Disabling automatic kernel updates** (if you rely on NVIDIA drivers):
  ```bash
  sudo apt-mark hold linux-image-generic linux-headers-generic
  ```
- **Using the official NVIDIA driver** (instead of Ubuntu's package) if compatibility is a recurring issue.

---

### **Final Notes**
- If the system becomes unbootable, use **GRUB** to select an older kernel.
- If NVIDIA drivers are critical for your workflow, consider using **LTS kernels** (non-HWE) for better stability.

Let me know if you need further assistance!

---

If you just want to proceed with `apt upgrade` and **skip the problematic packages**, you can temporarily exclude them from the upgrade process. Here’s how:

### **Option 1: Skip Broken Packages and Continue Upgrade**
Run:
```bash
sudo apt --fix-broken install
sudo apt upgrade -y --ignore-missing --allow-downgrades
```
- `--ignore-missing` skips unavailable packages.
- `--allow-downgrades` lets APT downgrade packages if needed.

### **Option 2: Hold (Block) Problematic Packages**
If the issue persists, **hold** (block) the problematic packages to prevent them from being upgraded:
```bash
sudo apt-mark hold linux-generic-hwe-22.04 linux-headers-generic-hwe-22.04 linux-image-6.8.0-60-generic
```
Then retry:
```bash
sudo apt upgrade -y
```

### **Option 3: Force Upgrade (Not Recommended)**
If you're okay with possibly breaking things further, force the upgrade:
```bash
sudo apt -o Dpkg::Options::="--force-overwrite" --fix-broken install
sudo apt upgrade -y
```
⚠️ **Warning:** This may cause instability if dependencies are mismatched.

### **After Skipping:**
- The system will still work, but the **NVIDIA driver might not function** on kernel `6.8.0-60`.
- You can **boot into an older kernel** (select it in GRUB) if needed.
- Once NVIDIA releases a compatible update, you can **unhold** the packages:
  ```bash
  sudo apt-mark unhold linux-generic-hwe-22.04 linux-headers-generic-hwe-22.04
  ```

Would you like help checking which kernel is currently active after the upgrade?
