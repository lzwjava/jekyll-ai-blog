---
audio: false
generated: true
lang: en
layout: post
title: Locating Your OpenJDK 21.0.7 Installation on Ubuntu 22.04
translated: false
type: note
---

The `java --version` command you ran shows that you have OpenJDK 21.0.7 installed on your system, specifically the version packaged for Ubuntu 22.04. This output confirms that the Java Development Kit (JDK) is installed and accessible from your command line.

The location of the Java installation can typically be found by checking where the `java` binary is located. Since you're on a Ubuntu-based system, the OpenJDK is likely installed in a standard system directory, such as `/usr/lib/jvm/`.

To locate the exact path of the Java installation:

1. **Find the path of the `java` binary**:
   Run the following command in your terminal:
   ```bash
   which java
   ```
   This will likely output something like `/usr/bin/java`. This is a symbolic link to the actual Java binary.

2. **Trace the symbolic link to the real location**:
   Since `/usr/bin/java` is usually a symlink, you can find the actual installation directory by running:
   ```bash
   readlink -f $(which java)
   ```
   This might output something like `/usr/lib/jvm/java-21-openjdk-amd64/bin/java`, indicating that the JDK is installed in `/usr/lib/jvm/java-21-openjdk-amd64/`.

3. **Verify the installation directory**:
   You can list the contents of the JVM directory to confirm:
   ```bash
   ls /usr/lib/jvm/
   ```
   You should see a directory like `java-21-openjdk-amd64` or similar, which contains the OpenJDK installation.

### Summary
Your Java installation is likely located in `/usr/lib/jvm/java-21-openjdk-amd64/` (or a similar directory under `/usr/lib/jvm/`). The `java` command you ran is a symlink pointing to the `java` binary within this directory. If you want to confirm the exact path, use the `readlink -f $(which java)` command.
