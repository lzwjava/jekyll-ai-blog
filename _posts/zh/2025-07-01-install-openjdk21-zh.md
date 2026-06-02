---
audio: false
generated: true
lang: zh
layout: post
title: 在macOS上升级至OpenJDK 21
translated: true
type: note
---

鉴于您当前在 macOS 系统上通过 Homebrew 安装了 OpenJDK 17，以下是在 2025 年 7 月 1 日这个时间点安装最新长期支持版 OpenJDK 21 的简明指南。您可以将 OpenJDK 21 与 OpenJDK 17 并行安装，并根据需要切换版本。推荐使用 Homebrew 安装，同时我也会提供手动安装方案。

### 方法一：使用 Homebrew 安装 OpenJDK 21（推荐）
您的系统已安装 Homebrew（当前 Java 版本可佐证），这是最便捷且易于维护的安装方式。

1. **更新 Homebrew**：
   确保 Homebrew 为最新状态以获取最新软件包：
   ```bash
   brew update
   ```

2. **安装 OpenJDK 21**：
   通过专用配方安装 OpenJDK 21：
   ```bash
   brew install openjdk@21
   ```
   该命令会以桶隔离方式安装，避免与其它 Java 版本冲突。

3. **配置 OpenJDK 21 路径**：
   按需选择临时或永久路径配置：
   - **临时配置（当前会话有效）**：
     ```bash
     export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
     ```
   - **永久配置（写入 shell 配置文件）**：
     编辑 Zsh 配置文件：
     ```bash
     nano ~/.zshrc
     ```
     添加以下行：
     ```bash
     export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
     ```
     保存后应用配置：
     ```bash
     source ~/.zshrc
     ```

4. **设置 JAVA_HOME 变量**：
   通过系统命令动态配置：
   ```bash
   export JAVA_HOME=$(/usr/libexec/java_home -v 21)
   ```
   永久配置方案：
   ```bash
   echo 'export JAVA_HOME=$(/usr/libexec/java_home -v 21)' >> ~/.zshrc
   source ~/.zshrc
   ```

5. **验证安装**：
   执行版本检查命令：
   ```bash
   java -version
   ```
   预期输出示例：
   ```
   openjdk 21.0.1 2023-10-17
   OpenJDK Runtime Environment (build 21.0.1+12)
   OpenJDK 64-Bit Server VM (build 21.0.1+12, mixed mode, sharing)
   ```

6. **多版本切换**：
   使用系统命令切换版本：
   - 切换至 OpenJDK 17：
     ```bash
     export JAVA_HOME=$(/usr/libexec/java_home -v 17)
     ```
   - 切换至 OpenJDK 21：
     ```bash
     export JAVA_HOME=$(/usr/libexec/java_home -v 21)
     ```
   也可使用 jenv 版本管理工具（通过 `brew install jenv` 安装）：
   ```bash
   jenv add /Library/Java/JavaVirtualMachines/openjdk-21.jdk/Contents/Home
   jenv add /Library/Java/JavaVirtualMachines/openjdk-17.jdk/Contents/Home
   jenv enable-plugin export
   jenv global 21
   ```

### 方法二：手动安装
若倾向不使用 Homebrew，可参考以下手动安装步骤。

1. **下载安装包**：
   - 访问 OpenJDK 官网（jdk.java.net/21）或 Oracle/Adoptium 等渠道
   - Apple Silicon 芯片选择 `macOS/AArch64` 版本，Intel 芯片选择 `macOS/x64` 版本

2. **校验文件完整性**：
   通过 SHA256 校验码验证：
   ```bash
   shasum -a 256 openjdk-21.0.1_macos-aarch64_bin.tar.gz
   ```

3. **解压安装包**：
   解压至目标目录（如用户主目录）：
   ```bash
   tar -xf openjdk-21.0.1_macos-aarch64_bin.tar.gz -C ~/OpenJDK
   ```
   完整路径将为 `~/OpenJDK/jdk-21.0.1.jdk/Contents/Home`

4. **移至系统目录（可选）**：
   为保持规范可移至标准目录：
   ```bash
   sudo mv ~/OpenJDK/jdk-21.0.1.jdk /Library/Java/JavaVirtualMachines/
   ```

5. **配置环境变量**：
   在 `~/.zshrc` 中追加：
   ```bash
   export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-21.0.1.jdk/Contents/Home
   export PATH=$JAVA_HOME/bin:$PATH
   ```
   应用配置：
   ```bash
   source ~/.zshrc
   ```

6. **验证安装**：
   最终确认安装结果：
   ```bash
   java -version
   ```

### 注意事项
- **芯片兼容性**：M1/M2 设备务必选择 AArch64 架构版本，Homebrew 会自动匹配对应架构
- **多版本管理**：所有 JDK 均安装在 `/Library/Java/JavaVirtualMachines/` 目录，可通过 `/usr/libexec/java_home -v <版本号>` 切换
- **Homebrew 优势**：支持一键更新（`brew upgrade openjd k@21`）并确保系统兼容性
- **替代发行版**：可选择 Azul Zulu 或 Eclipse Temurin 等 OpenJDK 21 发行版

若遇到安装问题，欢迎随时咨询![](https://www.geeksforgeeks.org/how-to-install-openjdk-in-macos/)[](https://formulae.brew.sh/formula/openjdk%4021)[](https://codetrips.com/2023/10/15/installing-java-jdk-21-macos/)
