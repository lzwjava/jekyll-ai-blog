---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 在 macOS 上安装 OpenJDK 8
translated: true
type: note
---

以下是在 **2025 年**于 macOS 上安装 **OpenJDK 8**（Java SE 8）的方法，涵盖 Homebrew、SDKMAN、手动安装程序和 MacPorts 等多种方式。无需复杂表格，只有清晰易懂的步骤：

---

## 1. 使用 Homebrew (`openjdk@8`)

这仍然是在 macOS 上安装 OpenJDK 8 最简单的方法之一。

### 步骤：

1. 打开终端。

2. 运行：

   ```bash
   brew install openjdk@8
   ```

   （[Homebrew Formulae][1]）

3. 安装完成后，链接 JDK 以便 macOS 工具能够检测到它：

   ```bash
   sudo ln -sfn $(brew --prefix)/opt/openjdk@8/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-8.jdk
   ```

   （[Homebrew Formulae][1]）

4. （可选）在你的 Shell 配置文件（例如 `.zshrc`）中将 OpenJDK 8 添加到 PATH：

   ```bash
   export PATH="$(brew --prefix openjdk@8)/bin:$PATH"
   ```

**注意，适用于 Apple Silicon（M 系列）用户：**
如果遇到架构问题，可能需要通过 Rosetta 2 运行 Homebrew：

```bash
env /usr/bin/arch -x86_64 /bin/zsh --login
brew install openjdk@8
```

然后继续执行符号链接和 PATH 设置（[Stack Overflow][2]）。

---

## 2. 通过 SDKMAN（Java 版本管理器）

SDKMAN 是一个灵活的工具，用于安装和切换多个 Java 版本。

### 快速安装：

```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk list java
sdk install java 8.xxx-tem
```

将 `8.xxx-tem` 替换为 `sdk list java` 中显示的标识符。（[Stack Overflow][2]）

---

## 3. 手动安装（Oracle / Adoptium / AdoptOpenJDK）

### 选项 A：Oracle 的 .dmg / .pkg 安装程序

1.  从 Oracle 的 Java SE 8 下载页面为你的架构下载正确的安装程序。
2.  打开 `.dmg`，运行 `.pkg` 安装程序，并按照提示操作。（[Oracle Documentation][3]）
3.  安装完成后，使用 `java_home` 等工具选择版本：

    ```bash
    /usr/libexec/java_home -v 1.8 --exec java -version
    ```

### 选项 B：AdoptOpenJDK 或类似构建

AdoptOpenJDK（现归于 Eclipse Adoptium）提供了构建版本——包括安装程序和归档文件选项。

*   例如，Salesforce 在 2025 年 8 月的文档中建议使用 AdoptOpenJDK 站点，选择 OpenJDK 8 (LTS) 和 HotSpot JVM，然后通过其安装程序进行安装。（[Salesforce][4]）

安装后，设置你的 JAVA\_HOME，例如：

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)
export PATH=$JAVA_HOME/bin:$PATH
```

---

## 4. MacPorts

如果你使用 MacPorts 而不是 Homebrew，安装 OpenJDK 8 很简单：

```bash
sudo port install openjdk8
```

查看安装内容：

```bash
port contents openjdk8
```

后续更新：

```bash
sudo port selfupdate && sudo port upgrade openjdk8
```

（[MacPorts][5]）

---

## 选择适合你的方法

| 需求场景                                           | 推荐方法                                        |
| -------------------------------------------------- | ----------------------------------------------- |
| 快速安装且易于维护                                 | **Homebrew (`brew install openjdk@8`)**         |
| 管理多个并发的 Java 版本                           | **SDKMAN**                                      |
| 完全控制且使用官方安装程序（偏好图形界面）         | **通过 Oracle/Adoptium 手动安装 `.dmg` 或 `.pkg`** |
| 偏好 MacPorts 生态系统                             | **MacPorts**                                    |

---

## 验证安装

安装后，使用以下命令检查：

```bash
java -version
```

预期看到类似 `"1.8.0_xxx"` 的输出，以确认 Java 8 已激活。如需精确控制：

```bash
/usr/libexec/java_home -v 1.8 --exec javac -version
```

---

## 最后总结

总而言之：

*   **Homebrew** 是 2025 年最流行的选择——只需 `brew install openjdk@8`，然后链接并设置 PATH。
*   **SDKMAN** 在你需要频繁切换 Java 版本时提供了灵活性。
*   **手动安装程序**（Oracle、Adoptium）仍然是一个可靠的、基于图形界面的备选方案。
*   **MacPorts** 适用于偏好该包管理器的用户。

如果你在设置 Shell 环境、切换 Java 版本或在此过程中遇到任何其他问题需要帮助，请随时告知！

[1]: https://formulae.brew.sh/formula/openjdk%408?utm_source=chatgpt.com "openjdk@8"
[2]: https://stackoverflow.com/questions/24342886/how-to-install-java-8-on-mac?utm_source=chatgpt.com "How to install Java 8 on Mac"
[3]: https://docs.oracle.com/javase/8/docs/technotes/guides/install/mac_jdk.html?utm_source=chatgpt.com "JDK 8 Installation for macOS"
[4]: https://help.salesforce.com/s/articleView?id=001117155&language=en_US&type=1&utm_source=chatgpt.com "How to Install OpenJDK 8 on macOS to Work with Anypoint ..."
[5]: https://ports.macports.org/port/openjdk8/?utm_source=chatgpt.com "Install openjdk8 on macOS with MacPorts"
