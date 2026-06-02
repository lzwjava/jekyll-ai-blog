---
audio: false
generated: true
lang: en
layout: post
title: Fixing 'Unsupported OpenJDK' Error in VisualVM
translated: false
type: note
---

The error "Version of OpenJDK is not supported. Please use the default-jdk" when running VisualVM indicates that the Java Development Kit (JDK) version being used is not compatible with VisualVM. This issue is common when VisualVM cannot find a supported JDK or when the installed JDK is not properly configured. Below are steps to resolve this issue, based on the context of your setup (YourKit Java Profiler 2025.3 and VisualVM on what appears to be a Linux system).

### Steps to Fix the Issue

1. **Check Your Current Java Version**
   Run the following command to verify the Java version installed:
   ```bash
   java -version
   ```
   This will display the OpenJDK version, such as:
   ```
   openjdk version "17.0.9" 2023-10-17
   OpenJDK Runtime Environment (build 17.0.9+9-Ubuntu-122.04)
   OpenJDK 64-Bit Server VM (build 17.0.9+9-Ubuntu-122.04, mixed mode, sharing)
   ```
   VisualVM typically requires a JDK (not just a JRE) and supports Oracle JDK 8+ or compatible OpenJDK versions. Ensure you have a supported JDK installed.[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)[](https://visualvm.github.io/troubleshooting.html)

2. **Install the Default JDK**
   The error suggests using the `default-jdk`. On Ubuntu/Debian, you can install it with:
   ```bash
   sudo apt update
   sudo apt install default-jdk
   ```
   This typically installs a stable, supported OpenJDK version (e.g., OpenJDK 11 or 17). After installation, verify the version again with `java -version`.[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)[](https://askubuntu.com/questions/1504020/visualvm-version-of-openjdk-is-not-supported)

3. **Set JAVA_HOME Environment Variable**
   VisualVM relies on the `JAVA_HOME` environment variable to locate the JDK. Check if it’s set:
   ```bash
   echo $JAVA_HOME
   ```
   If it’s not set or points to an unsupported JDK, set it to the correct JDK path. For example, if `default-jdk` installed OpenJDK 17, the path might be `/usr/lib/jvm/java-17-openjdk-amd64`. Set it with:
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
   ```
   To make this permanent, add the line to your `~/.bashrc` or `~/.zshrc`:
   ```bash
   echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
   source ~/.bashrc
   ```
   Replace the path with the actual JDK path on your system (use `update-alternatives --list java` to find it).[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)[](https://github.com/oracle/visualvm/issues/558)

4. **Specify JDK Path for VisualVM**
   If setting `JAVA_HOME` doesn’t resolve the issue, you can explicitly specify the JDK path when launching VisualVM:
   ```bash
   ~/bin/YourKit-JavaProfiler-2025.3/bin/visualvm --jdkhome /usr/lib/jvm/java-17-openjdk-amd64
   ```
   Replace `/usr/lib/jvm/java-17-openjdk-amd64` with the path to your JDK. This ensures VisualVM uses the specified JDK.[](https://visualvm.github.io/download.html)[](https://notepad.onghu.com/2021/solve-visualvm-does-not-start-on-windows-openjdk/)

5. **Install a Compatible JDK**
   If the `default-jdk` is still incompatible, consider installing a specific JDK version known to work with VisualVM, such as OpenJDK 11 or Oracle JDK 8+:
   ```bash
   sudo apt install openjdk-11-jdk
   ```
   Then, update `JAVA_HOME` or use the `--jdkhome` option as described above.[](https://stackoverflow.com/questions/78019430/visualvm-version-of-openjdk-is-not-supported)

6. **Check VisualVM Installation**
   Ensure VisualVM is correctly installed. The error suggests you’re running VisualVM from the YourKit Java Profiler directory (`~/bin/YourKit-JavaProfiler-2025.3/bin`). This is unusual, as VisualVM is typically a standalone tool or bundled with a JDK. Verify that VisualVM is not corrupted:
   - Download the latest VisualVM release from `visualvm.github.io/download.html` (e.g., VisualVM 2.2, released April 22, 2025, supports JDK 24).[](https://visualvm.github.io/relnotes.html)[](https://visualvm.github.io/)
   - Unzip it to a new directory and run it:
     ```bash
     unzip visualvm_22.zip
     cd visualvm_22/bin
     ./visualvm --jdkhome /usr/lib/jvm/java-17-openjdk-amd64
     ```
   Avoid unzipping over an existing VisualVM installation, as this can cause issues.[](https://visualvm.github.io/troubleshooting.html)

7. **Check for Multiple Java Installations**
   Multiple Java versions can cause conflicts. List all installed Java versions:
   ```bash
   update-alternatives --list java
   ```
   If multiple versions are listed, set the desired one as default:
   ```bash
   sudo update-alternatives --config java
   ```
   Select the number corresponding to the compatible JDK (e.g., OpenJDK 11 or 17).[](https://askubuntu.com/questions/1504020/visualvm-version-of-openjdk-is-not-supported)

8. **Verify VisualVM Dependencies**
   VisualVM requires `libnb-platform18-java` and `libvisualvm-jni`. Ensure these are installed:
   ```bash
   sudo apt install libnb-platform18-java libvisualvm-jni
   ```
   This is particularly relevant if you installed VisualVM via `apt`.[](https://askubuntu.com/questions/1504020/visualvm-version-of-openjdk-is-not-supported)

9. **Bypass OpenJDK Restrictions (Optional)**
   If you’re using an unsupported OpenJDK build (e.g., IcedTea or AdoptOpenJDK), profiling features may be limited. You can bypass some restrictions by adding a command-line argument:
   ```bash
   ./visualvm --jdkhome /usr/lib/jvm/java-17-openjdk-amd64 -J-Dorg.graalvm.visualvm.profiler.SupportAllVMs=true
   ```
   This enables profiling for unsupported JVMs, though it’s not guaranteed to work perfectly.[](https://github.com/oracle/visualvm/issues/143)

10. **Check YourKit and VisualVM Compatibility**
    Since you’re running VisualVM from the YourKit Java Profiler directory, ensure YourKit’s environment isn’t interfering. YourKit Java Profiler 2025.3 may bundle a specific VisualVM version or configuration. Check YourKit’s documentation or contact `support@yourkit.com` to confirm compatibility with your JDK. Alternatively, try running VisualVM independently (downloaded separately) to isolate the issue.[](https://www.yourkit.com/changes/)

### Additional Notes
- **YourKit Context**: The error doesn’t directly relate to YourKit Java Profiler, but running VisualVM from YourKit’s directory suggests integration. YourKit supports Java 7–15 and later versions with EAP builds, so ensure your JDK is compatible with both tools if they’re used together.[](https://www.yourkit.com/forum/viewtopic.php?t=41723)[](https://www.yourkit.com/forum/viewtopic.php?t=40299)
- **Log Files**: Check VisualVM logs for more details. Logs are typically in `~/.visualvm/<version>/var/log`. For YourKit, check `~/.yjp/log/` for profiler agent logs. If issues persist, send logs to `support@yourkit.com`.[](https://stackoverflow.com/questions/70211315/java-17-and-yourkit-2021-11)[](https://www.yourkit.com/forum/viewtopic.php?t=40299)
- **Alternative**: If VisualVM continues to fail, consider using YourKit’s built-in profiling tools or another profiler like JProfiler or Async Profiler, which may have better compatibility with your setup.[](https://digma.ai/9-best-java-profilers-to-use-in-2024/)[](https://bell-sw.com/blog/a-guide-to-java-profiling-tools-techniques-best-practices/)

### If the Issue Persists
If none of the above resolves the issue, please provide:
- Output of `java -version` and `echo $JAVA_HOME`.
- Output of `update-alternatives --list java`.
- The exact VisualVM version (check via `visualvm --help` or the download page).
- Whether you’re using VisualVM bundled with YourKit or a standalone installation.

This will help pinpoint the issue further. You can also report the issue to the VisualVM GitHub page (`https://github.com/oracle/visualvm`) or YourKit support for specific guidance.[](https://github.com/oracle/visualvm/issues/558)
