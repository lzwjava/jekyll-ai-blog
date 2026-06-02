---
audio: false
generated: true
lang: en
layout: post
title: Installing YourKit Java Profiler on Ubuntu
translated: false
type: note
---

To install YourKit Java Profiler on Ubuntu, follow these steps based on the information available from the YourKit website:

1. **Download the Profiler**:
   - Visit the YourKit Java Profiler download page at [https://www.yourkit.com/java/profiler/download/](https://www.yourkit.com/java/profiler/download/).[](https://www.yourkit.com/java/profiler/download/)
   - Select the Linux version of YourKit Java Profiler 2025.3, which supports Java 8 to Java 24 and is compatible with Linux (including Ubuntu) on architectures like arm32, arm64, ppc64le, x64, and x86. Ensure your system meets the [system requirements](https://www.yourkit.com/docs/java/system-requirements/) for compatibility.[](https://www.yourkit.com/java/profiler/download/)

2. **Download the Archive**:
   - Download the `.zip` archive for Linux (e.g., `YourKit-JavaProfiler-2025.3-<build>.zip`). The download link is available on the YourKit download page.[](https://www.yourkit.com/download/yjp_2025_3_builds.jsp)

3. **Unzip the Archive**:
   - Open a terminal and navigate to the directory where the downloaded file is located (e.g., `~/Downloads`).
   - Unzip the archive using the following command:
     ```bash
     unzip YourKit-JavaProfiler-2025.3-<build>.zip -d /opt/yourkit
     ```
     Replace `<build>` with the actual build number from the downloaded file. This command extracts the profiler to `/opt/yourkit`. You can choose another directory if preferred.[](https://www.yourkit.com/docs/java-profiler/latest/help/installation.jsp)

4. **Run the Profiler**:
   - Navigate to the extracted directory:
     ```bash
     cd /opt/yourkit
     ```
   - Run the profiler using the provided script:
     ```bash
     ./bin/profiler.sh
     ```
     This launches the YourKit Java Profiler user interface.[](https://www.yourkit.com/docs/java-profiler/latest/help/installation.jsp)

5. **Optional: Unattended Installation with License Key**:
   - If you have a license key and want to automate the installation, you can use command-line options to accept the EULA and apply the license key. For example:
     ```bash
     ./bin/profiler.sh -accept-eula -license-key=<key>
     ```
     Replace `<key>` with your actual license key. This is useful for automation or scripted setups.[](https://www.yourkit.com/docs/java-profiler/latest/help/installation.jsp)

6. **Integrate with Development Environment (Optional)**:
   - If you use an IDE like Eclipse, IntelliJ IDEA, or NetBeans, YourKit provides plugins for seamless integration. For Eclipse, for example:
     - Open Eclipse and go to **Help > Install New Software**.
     - Add the YourKit plugin repository: `https://www.yourkit.com/download/yjp2025_3_for_eclipse/`.
     - Select the YourKit Java Profiler plugin, follow the installation prompts, and restart Eclipse if required.
     - Alternatively, use the offline archive at `<Profiler Installation Directory>/lib/eclipse-plugin/yjp2025_3_for_eclipse.zip`.[](https://www.yourkit.com/docs/java-profiler/latest/help/eclipse.jsp)
   - After installation, the "Profile" action will appear in Eclipse’s toolbar, main menu, or context menus for easy profiling.[](https://www.yourkit.com/docs/java-profiler/latest/help/eclipse.jsp)

7. **Verify Installation**:
   - Once the profiler is running, the welcome screen will allow you to monitor locally running Java applications, connect to remote applications, or open existing snapshots. You can also load a demo application to explore the profiler’s features.[](https://yourkit-java-profiler.findmysoft.com/)

8. **Additional Notes**:
   - If you encounter issues, ensure Java (version 8 or higher) is installed on your system, as YourKit Java Profiler requires a compatible JVM. You can check your Java version with:
     ```bash
     java -version
     ```
   - For remote profiling, ensure SSH access is configured if profiling applications on remote servers.[](https://www.yourkit.com/java/profiler/)
   - YourKit offers a 15-day free trial, so no license key is required initially. For non-commercial open-source projects, you can contact YourKit sales for a free license.[](https://www.yourkit.com/java/profiler/download/)[](https://bahmni.atlassian.net/wiki/spaces/BAH/pages/3125838019/Remote%2BJava%2BProfiling%2Busing%2BYourKit)
   - If the profiler fails to start (e.g., due to spaces in the installation directory), move the extracted folder to a path without spaces, such as `/opt/yourkit`.[](https://www.yourkit.com/changes/)

For further assistance, refer to the [YourKit documentation](https://www.yourkit.com/docs/java/) or contact their support via the [YourKit website](https://www.yourkit.com/support/).[](https://www.yourkit.com/docs/)

Let me know if you need help with any specific step!
