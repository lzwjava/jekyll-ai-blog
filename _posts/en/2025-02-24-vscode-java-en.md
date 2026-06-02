---
audio: false
generated: true
lang: en
layout: post
title: Configure the Java Compiler in Visual Studio Code
translated: false
type: note
---

Hey there! To configure the Java compiler in Visual Studio Code (VSCode) version 1.96.4 on Windows, especially since you’ve already installed the Java Extension Pack, you’ll need to set up the Java Development Kit (JDK) path. The Java compiler is part of the JDK, and VSCode needs to know where to find it to compile your Java code. Here’s a step-by-step guide to get you set up:

---

### Step 1: Ensure You Have a JDK Installed
Before configuring anything in VSCode, make sure you have a JDK (not just a JRE) installed on your Windows machine. The JDK includes the Java compiler (`javac`). If you haven’t installed it yet, you can download it from a provider like Oracle, OpenJDK, or Adoptium (e.g., JDK 17 or another version compatible with your project). After installing, note the installation path (e.g., `C:\Program Files\Java\jdk-17.0.1`).

---

### Step 2: Open VSCode Settings
To tell VSCode where your JDK is located, you’ll need to adjust its settings:

- **Via the Settings UI:**
  - Press `Ctrl + ,` to open the Settings panel.
  - Alternatively, go to `File > Preferences > Settings`.
- **Via settings.json (optional):**
  - Press `Ctrl + Shift + P` to open the Command Palette.
  - Type **"Open Settings (JSON)"** and select it to edit the `settings.json` file directly.

---

### Step 3: Set the JDK Path with `java.home`
The Java Extension Pack relies on the `java.home` setting to locate your JDK for compilation and language features (like IntelliSense). Here’s how to configure it:

- **In the Settings UI:**
  - In the Settings panel, search for **"java.home"**.
  - In the "Java: Home" field, enter the full path to your JDK installation. For example:
    ```
    C:\Program Files\Java\jdk-17.0.1
    ```
  - Use backslashes (`\`) since you’re on Windows, and ensure the path points to the JDK root directory (it should contain a `bin` folder with `javac.exe`).

- **In settings.json:**
  - If you’re editing `settings.json`, add this line (replace the path with your actual JDK location):
    ```json
    "java.home": "C:\\Program Files\\Java\\jdk-17.0.1"
    ```
  - Example full `settings.json`:
    ```json
    {
        "java.home": "C:\\Program Files\\Java\\jdk-17.0.1"
    }
    ```
  - Save the file after editing.

---

### Step 4: Verify the Path
Double-check that:
- The path points to a JDK (not a JRE). The JDK’s `bin` folder should include `javac.exe`.
- There are no typos in the path, and it matches your JDK installation location (e.g., `C:\Program Files\Java\jdk-17.0.1`).

If you’re unsure where your JDK is installed, you can find it in `C:\Program Files\Java` or wherever you chose during installation.

---

### Step 5: Optional - Configure Multiple JDKs
If you have multiple JDK versions installed and want to switch between them (e.g., JDK 8 for one project, JDK 17 for another), you can use the `java.configuration.runtimes` setting:

- Add this to your `settings.json`:
  ```json
  "java.configuration.runtimes": [
      {
          "name": "JavaSE-1.8",
          "path": "C:\\Program Files\\Java\\jdk1.8.0_291"
      },
      {
          "name": "JavaSE-17",
          "path": "C:\\Program Files\\Java\\jdk-17.0.1",
          "default": true
      }
  ]
  ```
- The `default: true` option sets the default runtime for running your code. However, for compilation, the Java extension primarily uses the JDK specified in `java.home`.

---

### Step 6: Reload or Restart VSCode
After setting `java.home`, you might need to:
- Reload the VSCode window (press `Ctrl + Shift + P`, type **"Reload Window"**, and select it).
- Or fully restart VSCode for the changes to take effect.

---

### Notes on Compilation
- **Single Java Files:** If you’re working with individual `.java` files (no build tools), the Java Extension Pack’s "Language Support for Java(TM) by Red Hat" uses the JDK from `java.home` to compile and run your code. You can use the "Run" button or the **"Java: Run"** command.
- **Projects with Build Tools:** If you’re using Maven, Gradle, or another build tool, the compiler is managed by the build tool’s configuration (e.g., `JAVA_HOME` environment variable, `pom.xml` for Maven, or `build.gradle` for Gradle). However, setting `java.home` still ensures VSCode’s language features work correctly.

---

### Troubleshooting
- **Path Issues:** If VSCode can’t find the JDK, double-check the path in `java.home`. Avoid extra spaces or quotes unless necessary.
- **JDK Not Installed:** If you get errors about missing `javac`, ensure a JDK is installed.
- **Version Compatibility:** Make sure your JDK version matches your project’s requirements (e.g., JDK 8, 11, 17).

---

That’s it! You should now have the Java compiler configured in VSCode. If you run into any issues or have more questions—like working with a specific build tool—feel free to let me know, and I’ll be happy to assist further! 😊

---

Set `maven.terminal.userJavaHome` to true. You can check the Java version in the terminal.
