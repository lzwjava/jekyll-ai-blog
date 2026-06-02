---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: CMake Usage and Explanation on Windows
translated: false
type: note
---

Great question! Let’s walk through what **CMake** is, how to use it—particularly on **Windows**, and what commands like `cmake --build` actually mean.

---

### 🔹 What is CMake?
- **CMake** is a cross-platform build system generator.
- It does **not** build projects itself—it creates the appropriate build files (like Visual Studio solutions, Makefiles, Ninja files, etc.) for your platform and compiler.
- Then, you use those generated files (or CMake’s own build driver) to actually compile your project.

---

### 🔹 Installing CMake on Windows
1. Download from: [https://cmake.org/download/](https://cmake.org/download/)
2. Install, and make sure **“Add CMake to system PATH”** is checked (or add manually).
3. Verify in a terminal (PowerShell or CMD):
   ```sh
   cmake --version
   ```

---

### 🔹 Typical CMake Workflow on Windows

Let’s say your project has:
```
project_root/
 ├─ CMakeLists.txt
 └─ src/
     └─ main.cpp
```

#### 1. Open a terminal
(You can use **x64 Native Tools Command Prompt for VS** if using MSVC, or just normal PowerShell if using `MinGW`/`Ninja`.)

#### 2. Create a build directory
It’s best to separate source and build:
```sh
cd project_root
mkdir build
cd build
```

#### 3. Generate build system files
Example with Visual Studio:
```sh
cmake .. -G "Visual Studio 17 2022" -A x64
```

Example with Ninja:
```sh
cmake .. -G Ninja
```

This step reads `../CMakeLists.txt` and generates the necessary build definitions.

#### 4. Build the project
Now you can use:
```sh
cmake --build .
```

- On Windows with Visual Studio, this actually calls `MSBuild` under the hood.
- With Ninja, it calls the `ninja` tool.

You can also tell CMake to build in **Release** mode:
```sh
cmake --build . --config Release
```
⚠ Note: `--config` is only used with multi-config generators (Visual Studio, Xcode). If you use Ninja or Makefiles, you specify at configuration:
```sh
cmake .. -DCMAKE_BUILD_TYPE=Release
```

#### 5. Run your executable
After building, look in the appropriate directory:
- For **Visual Studio**: `build/Debug/` or `build/Release/`
- For **Ninja**: just inside `build/`

---

### 🔹 Common Commands Cheat Sheet
```sh
# Configure project (generate build files)
cmake -S . -B build

# Configure with Release build type (single-config generator)
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release

# Build project
cmake --build build

# Build with specific config (for Visual Studio/Xcode)
cmake --build build --config Release

# Install compiled outputs (if defined in CMakeLists)
cmake --install build
```

---

✅ **Summary**:
- **`cmake ..`** → Configure and generate platform-specific project/build files.
- **`cmake --build .`** → Actually compiles using the chosen build tool.
- On Windows, you’ll often use **Visual Studio generators** or **Ninja** for better performance.

---

Would you like me to give you a **minimal example CMakeLists.txt** and walk through building a simple C++ “Hello World” project on Windows step-by-step?
