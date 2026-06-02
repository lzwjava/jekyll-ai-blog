---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GraalVM Installation and Usage Guide
translated: false
type: note
---

## What is GraalVM?

GraalVM is an open-source high-performance runtime (JDK distribution) that supports multiple programming languages like Java, JavaScript, Python, and more. It features an advanced JIT compiler for faster execution and the ability to compile Java applications to native executables via Native Image, reducing startup time and memory footprint.

## Installation

1. **Download GraalVM**:
   - Go to the official GraalVM downloads page.
   - Choose the Community Edition (free) or Oracle GraalVM (with additional features).
   - Select the version for your platform (e.g., Linux, macOS, Windows) and architecture (x64 or ARM).
   - As of 2025, the latest stable release is GraalVM for JDK 22 or 23—check the site for the most current.

2. **Extract and Install**:
   - Unzip the downloaded archive to a directory, e.g., `/opt/graalvm` on Linux/macOS or `C:\Program Files\GraalVM` on Windows.
   - No installer is needed; it's a portable distribution.

3. **Set Environment Variables**:
   - Set `JAVA_HOME` to the GraalVM directory (e.g., `export JAVA_HOME=/opt/graalvm` on Linux/macOS).
   - Add the `bin` directory to your `PATH` (e.g., `export PATH=$JAVA_HOME/bin:$PATH`).
   - Verify with `java -version`; it should show GraalVM details.

4. **Install Additional Components (Optional)**:
   - Use `gu` (GraalVM Updater) for language runtimes or Native Image: `gu install native-image` (requires build tools like `build-essential` on Linux).

## Building a Hello World Program

We'll use Java for this example, as it's GraalVM's primary language. Create a simple "Hello World" app, compile it, and run it.

### Step 1: Write the Code

Create a file named `HelloWorld.java`:

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World from GraalVM!");
    }
}
```

### Step 2: Compile

Open a terminal in the directory with the file and run:

```
javac HelloWorld.java
```

This produces `HelloWorld.class`.

### Step 3: Run

```
java HelloWorld
```

Output:

```
Hello, World from GraalVM!
```

### Advanced: Compile to Native Executable

GraalVM's Native Image feature lets you build a standalone binary.

1. Ensure Native Image is installed: `gu install native-image`.
2. Generate a configuration (first run may require this):

   ```
   native-image --no-fallback -H:+ReportExceptionStackTraces HelloWorld
   ```

   - This creates `HelloWorld` (or `helloworld.exe` on Windows), a native binary.
   - On first build, it analyzes the app and may take a few minutes.

3. Run the native binary:

   ```
   ./HelloWorld
   ```

   Output is the same, but it starts instantly with low memory use.

## Tips for Using GraalVM

- **Switching JDKs**: Use SDKMAN! (`sdk install java 22.0.2-graal`) for easy management.
- **Multi-Language**: Run Node.js code with `node` from GraalVM, or Python with `python`.
- **Performance**: Enable GraalVM's JIT with `-XX:+UnlockExperimentalVMOptions -XX:+UseJVMCICompiler`.
- **Troubleshooting**: Check logs in `~/.gu/` for issues; ensure your system has a C compiler for Native Image.

For more details, see the official docs.

[GraalVM Downloads](https://www.graalvm.org/downloads/)
[GraalVM User Guide](https://www.graalvm.org/latest/reference-manual/)
[Native Image Tutorial](https://www.graalvm.org/latest/reference-manual/native-image/)
