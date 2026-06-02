---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Ubuntu 上安装 OpenJDK 24
translated: true
type: note
---

Question: 如何在 Ubuntu 上安装 OpenJDK 24？

Answer:

OpenJDK 24 **不是**一个 LTS 版本（它是一个短期/特性发布版本，仅提供约 6 个月的支持）。Ubuntu LTS 版本（如 24.04）通常在官方仓库中只包含 OpenJDK 的 LTS 版本（目前是 OpenJDK 21，以及未来可用的 OpenJDK 25）。

截至 2026 年初，OpenJDK 24 在 Ubuntu 24.04 的标准仓库中**不可用**。不过，你有几种可靠的选择来进行安装：

### 推荐选项：从 jdk.java.net 下载官方 OpenJDK 24 二进制文件（干净且简单）

```bash
# 1. 访问官方存档页面
#    https://jdk.java.net/archive/
#    → 找到 JDK 24 → Linux / x64 → 下载 .tar.gz 文件

# 示例（如有需要，请替换为实际文件名）
wget https://download.java.net/java/GA/jdk24/5f/f8/3a5f8c3a5f8c3a5f8c3a5f8c3a5f8c3a/36/GPL/openjdk-24_linux-x64_bin.tar.gz

# 2. 解压文件
sudo mkdir -p /usr/lib/jvm
sudo tar xf openjdk-24_linux-x64_bin.tar.gz -C /usr/lib/jvm/
# → 将创建目录 /usr/lib/jvm/jdk-24

# 3. 设置为默认版本（可选 – 使用 update-alternatives）
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-24/bin/java 2400 \
  --slave /usr/bin/javac javac /usr/lib/jvm/jdk-24/bin/javac \
  --slave /usr/bin/jar jar /usr/lib/jvm/jdk-24/bin/jar

sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk-24/bin/javac 2400

# 4. 选择版本
sudo update-alternatives --config java
# 选择 jdk-24 版本

# 5. 验证
java --version
# 应该显示 openjdk 24.x ...
```

### 备选方案：使用带有 .deb 软件包的第三方构建版本（更容易升级）

通常为非 LTS 版本提供优质 .deb 软件包的流行供应商包括：

- **Azul Zulu**（非常可靠，免费，通过 TCK 认证）
  - 访问 → https://www.azul.com/downloads/?version=java-24
  - 选择 Linux / Ubuntu / .deb / JDK → 下载并安装：

  ```bash
  sudo dpkg -i zulu24.xx.x_linux_amd64.deb
  ```

- **Eclipse Temurin** (Adoptium)
  - https://adoptium.net/temurin/releases/?version=24
  - 选择 .deb 软件包

- **Microsoft Build of OpenJDK**
  - https://learn.microsoft.com/en-us/java/openjdk/install
  - 他们有时会通过自己的 repo 提供较新版本

### 如果你在某些 PPA 或 Ubuntu 的 devel/unstable 仓库中看到 openjdk-24-jdk

在某些情况下（尤其是较新 Ubuntu 版本的开发周期中），`openjdk-24-jdk` 可能会暂时出现。你可以检查：

```bash
apt search openjdk-24
```

如果没有任何显示 → 请使用上述方法之一。

### 快速总结 – 大多数人会选择这两种方式之一：

1. 来自 jdk.java.net 的官方 tar.gz（最干净，无需额外的 repo）
2. Azul .deb 软件包（最容易安装和更新）

安装完成后，如果你的工具需要，请记得设置 `JAVA_HOME`：

```bash
export JAVA_HOME=/usr/lib/jvm/jdk-24
# 或者如果使用 Azul: /usr/lib/jvm/zulu24-ca-amd64
```

将其添加到 `~/.bashrc` 或 `/etc/environment` 以使设置永久生效。

References:

- [https://jdk.java.net/archive/](https://jdk.java.net/archive/)
- [https://ubuntuhandbook.org/index.php/2025/03/install-openjdk-24-ubuntu](https://ubuntuhandbook.org/index.php/2025/03/install-openjdk-24-ubuntu)
- [https://www.azul.com/downloads/](https://www.azul.com/downloads/)
- [https://adoptium.net/temurin/releases/](https://adoptium.net/temurin/releases/)
