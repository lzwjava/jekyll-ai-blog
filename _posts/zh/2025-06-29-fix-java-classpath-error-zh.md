---
audio: false
generated: true
lang: zh
layout: post
title: 修复Java类路径错误
translated: true
type: note
---

您遇到的错误（`Could not find or load main class scripts.benchmark.MultiMark`）是因为您尝试从项目根目录（`~/projects/lzwjava.github.io`）使用完全限定类名（`scripts.benchmark.MultiMark`）运行Java程序，但Java运行时期望从包结构开始的目录运行该类，或者您需要正确指定类路径。当您切换到`scripts/benchmark`目录并运行`java MultiMark`时，它成功了，因为该类相对于命令位于正确的目录中。

要从项目根目录（`~/projects/lzwjava.github.io`）运行`MultiMark.java`或`MultiMark.class`而不切换目录，您可以使用`-cp`（类路径）选项与`java`命令告诉Java在哪里找到编译后的类文件。以下是两种实现方法，让您保持在根目录：

---

### **选项1：使用类路径运行编译后的类**

如果`MultiMark.class`已存在于`scripts/benchmark/`中（如您的`ls`输出所示），您可以通过指定类路径从根目录运行它。

1. **保持在根目录**
   确保您在`~/projects/lzwjava.github.io`中。

2. **运行程序**
   使用`-cp`选项指向包含类文件的目录：

   ```bash
   java -cp scripts/benchmark MultiMark
   ```

   - `-cp scripts/benchmark`告诉Java在`scripts/benchmark`目录中查找类。
   - `MultiMark`是类名（没有`.class`或包前缀，因为`MultiMark.java`没有`package`语句）。

   这应该产生如下输出：

   ```
   CPU cores: 32
   ...
   ```

3. **注意**：如果`MultiMark.class`已过时或缺失，首先从根目录编译源文件：

   ```bash
   javac scripts/benchmark/MultiMark.java
   ```

   然后运行上述命令。

---

### **选项2：使用类路径直接运行源文件（Java 11+）**

如果您更喜欢直接运行源文件（如`python script.py`），您可以使用`java`命令与源文件路径，并指定类路径。

1. **保持在根目录**
   确保您在`~/projects/lzwjava.github.io`中。

2. **运行源文件**
   使用：

   ```bash
   java -cp scripts/benchmark scripts/benchmark/MultiMark.java
   ```

   - `-cp scripts/benchmark`将类路径设置为包含源的目录。
   - `scripts/benchmark/MultiMark.java`指定要编译和运行的源文件。

   这在一个步骤中编译并运行`MultiMark.java`，产生与之前相同的输出。

---

### **选项3：在根目录中创建Shell脚本**

为了更方便（如从根目录运行`./multimark`），您可以在根目录（`~/projects/lzwjava.github.io`）中创建一个Shell脚本。

1. **创建Shell脚本**
   在根目录中创建一个名为`multimark`的文件：

   ```bash
   nano multimark
   ```

   添加：

   ```bash
   #!/bin/bash
   java -cp scripts/benchmark MultiMark
   ```

   保存并退出。

2. **使其可执行**

   ```bash
   chmod +x multimark
   ```

3. **运行脚本**
   从根目录：

   ```bash
   ./multimark
   ```

   这运行Java程序而不需要切换目录。

4. **可选：在脚本中编译**
   如果您希望脚本处理编译（例如，如果源文件更改），修改脚本：

   ```bash
   #!/bin/bash
   javac scripts/benchmark/MultiMark.java
   java -cp scripts/benchmark MultiMark
   ```

---

### **关键注意事项**

- **类路径（`-cp`）**：`-cp`选项告诉Java在哪里查找类或源文件。由于`MultiMark.java`没有`package`语句，类名只是`MultiMark`，而不是`scripts.benchmark.MultiMark`。如果它有`package scripts.benchmark;`行，您需要从根目录使用`java -cp . scripts.benchmark.MultiMark`。
- **Java版本**：源文件执行（`java scripts/benchmark/MultiMark.java`）需要Java 11或更高版本。您的系统似乎已安装Java，因为从`scripts/benchmark`目录运行成功。
- **目录**：这些解决方案让您保持在根目录（`~/projects/lzwjava.github.io`），符合您的偏好。
- **自动化**：Shell脚本（选项3）最接近Python式的体验，因为您可以像运行Python脚本一样运行`./multimark`。您还可以将其添加到`PATH`中以全局访问，但这是可选的。
- **错误处理**：如果您遇到如`NoClassDefFoundError`的错误，请确保`MultiMark.class`存在于`scripts/benchmark/`中或重新编译。如果找不到Java，请验证安装（`java --version`）。

如果您希望将此与Python脚本集成或需要特定的工作流程（例如，一起运行`multimark.py`和`MultiMark.java`），请告诉我！
