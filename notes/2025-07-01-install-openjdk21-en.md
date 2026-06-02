---
audio: false
generated: true
lang: en
layout: post
title: Upgrade to OpenJDK 21 on macOS
translated: false
type: note
---

Since you currently have OpenJDK 17 installed via Homebrew on your macOS system, here’s a concise guide to install OpenJDK 21, which is the latest Long Term Support (LTS) release as of your current date, July 1, 2025. You can install OpenJDK 21 alongside OpenJDK 17 and switch between them as needed. The simplest method is using Homebrew, but I’ll also provide a manual installation option.

### Method 1: Install OpenJDK 21 Using Homebrew (Recommended)

Homebrew is already installed on your system, as indicated by your current Java version. This is the easiest and most maintainable approach.

1. **Update Homebrew**:
   Ensure Homebrew is up to date to fetch the latest packages:

   ```bash
   brew update
   ```

2. **Install OpenJDK 21**:
   Homebrew provides a specific formula for OpenJDK 21. Run the following command:

   ```bash
   brew install openjdk@21
   ```

   This installs OpenJDK 21 in a keg-only manner, meaning it won’t be symlinked into `/usr/local/bin` to avoid conflicts with other Java versions.

3. **Add OpenJDK 21 to Your Path**:
   To use OpenJDK 21, you need to add it to your system’s PATH. Homebrew will provide instructions after installation, but typically, you can link it temporarily or permanently:
   - **Temporary (for the current session)**:

     ```bash
     export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
     ```

   - **Permanent (add to shell configuration)**:
     Open your shell configuration file (likely `~/.zshrc` since macOS uses Zsh by default):

     ```bash
     nano ~/.zshrc
     ```

     Add the following line:

     ```bash
     export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
     ```

     Save and close the file, then apply the changes:

     ```bash
     source ~/.zshrc
     ```

4. **Set JAVA_HOME**:
   To ensure Java applications can locate OpenJDK 21, set the `JAVA_HOME` environment variable:

   ```bash
   export JAVA_HOME=$(/usr/libexec/java_home -v 21)
   ```

   Add this to your `~/.zshrc` for permanence:

   ```bash
   echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 21)' >> ~/.zshrc
   source ~/.zshrc
   ```

5. **Verify Installation**:
   Check that OpenJDK 21 is installed and active:

   ```bash
   java -version
   ```

   You should see output similar to:

   ```
   openjdk 21.0.1 2023-10-17
   OpenJDK Runtime Environment (build 21.0.1+12)
   OpenJDK 64-Bit Server VM (build 21.0.1+12, mixed mode, sharing)
   ```

6. **Switching Between Java Versions**:
   Since you have OpenJDK 17 installed, you can switch between versions using `/usr/libexec/java_home`. For example:
   - To use OpenJDK 17:

     ```bash
     export JAVA_HOME=$(/usr/libexec/java_home -v 17)
     ```

   - To use OpenJDK 21:

     ```bash
     export JAVA_HOME=$(/usr/libexec/java_home -v 21)
     ```

   Alternatively, consider using a version manager like `jenv` (install via `brew install jenv`) for easier switching:

   ```bash
   jenv add /Library/Java/JavaVirtualMachines/openjdk-21.jdk/Contents/Home
   jenv add /Library/Java/JavaVirtualMachines/openjdk-17.jdk/Contents/Home
   jenv enable-plugin export
   jenv global 21
   ```

### Method 2: Manual Installation

If you prefer not to use Homebrew, you can manually install OpenJDK 21.

1. **Download OpenJDK 21**:
   - Visit the official OpenJDK website (jdk.java.net/21) or a trusted provider like Oracle, Azul, or Adoptium.
   - For Apple Silicon (M1/M2), download the `macOS/AArch64` tar.gz file. For Intel-based Macs, choose `macOS/x64`.
   - Example: From Oracle’s JDK 21 download page, select the ARM64 or x64 tar.gz file.

2. **Verify the Download**:
   Check the integrity of the downloaded file using its SHA256 checksum:

   ```bash
   shasum -a 256 openjdk-21.0.1_macos-aarch64_bin.tar.gz
   ```

   Compare the output with the checksum provided on the download page.

3. **Extract the File**:
   Extract the tar.gz file to a desired directory, such as your home directory:

   ```bash
   tar -xf openjdk-21.0.1_macos-aarch64_bin.tar.gz -C ~/OpenJDK
   ```

   The JDK will be extracted to `~/OpenJDK/jdk-21.0.1.jdk/Contents/Home`.

4. **Move to System Directory** (Optional):
   For consistency, you can move the JDK to the standard macOS Java directory:

   ```bash
   sudo mv ~/OpenJDK/jdk-21.0.1.jdk /Library/Java/JavaVirtualMachines/
   ```

5. **Set JAVA_HOME and PATH**:
   Update your `~/.zshrc` to include:

   ```bash
   export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.0.1.jdk/Contents/Home
   export PATH=$JAVA_HOME/bin:$PATH
   ```

   Apply the changes:

   ```bash
   source ~/.zshrc
   ```

6. **Verify Installation**:
   Confirm the installation:

   ```bash
   java -version
   ```

   Ensure it shows OpenJDK 21.

### Notes

- **Apple Silicon Compatibility**: Ensure you download the AArch64 build for M1/M2 Macs to avoid performance issues. Homebrew automatically selects the correct architecture.
- **Multiple JDKs**: macOS supports multiple JDKs in `/Library/Java/JavaVirtualMachines/`. Use `/usr/libexec/java_home -v <version>` to switch between them.
- **Homebrew Advantage**: Homebrew simplifies updates (`brew upgrade openjdk@21`) and ensures compatibility with your system.
- **Alternative Providers**: You can also use Azul Zulu or Eclipse Temurin builds of OpenJDK 21, available from their respective websites (e.g., azul.com or adoptium.net).

If you encounter issues, let me know, and I can help troubleshoot![](https://www.geeksforgeeks.org/how-to-install-openjdk-in-macos/)[](https://formulae.brew.sh/formula/openjdk%4021)[](https://codetrips.com/2023/10/15/installing-java-jdk-21-macos/)
