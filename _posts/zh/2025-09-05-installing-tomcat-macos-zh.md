---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 macOS 上安装 Apache Tomcat
translated: true
type: note
---

以下是在 **macOS 上安装和运行 Apache Tomcat** 的逐步指南：

---

### 1. 检查 Java 环境

Tomcat 需要 Java 环境。请先验证是否已安装：

```bash
java -version
```

如果未显示 Java 版本（例如 `1.8` 或 `11` 及以上），请安装 Java。在 macOS 上最简单的方式是通过 [Homebrew](https://brew.sh)：

```bash
brew install openjdk@11
```

然后链接安装的 Java：

```bash
brew link --force --overwrite openjdk@11
```

---

### 2. 安装 Tomcat（方案 A：使用 Homebrew —— 最便捷）

通过 Homebrew 可快速安装 Tomcat：

```bash
brew install tomcat
```

这通常会安装最新版本（例如 Tomcat 10）。

安装位置通常为：

```
/usr/local/Cellar/tomcat/<版本号>/libexec
```

若使用 Apple Silicon 芯片：

```
/opt/homebrew/Cellar/tomcat/<版本号>/libexec
```

运行 Tomcat：

```bash
catalina run
```

---

### 3. 安装 Tomcat（方案 B：手动下载 —— 官方方式）

1. 访问 [Apache Tomcat 官网](https://tomcat.apache.org/download-10.cgi)，下载最新稳定版（选择 `.tar.gz` 格式）。

2. 解压至目标目录，例如：

   ```bash
   tar xvf apache-tomcat-10.*.tar.gz
   mv apache-tomcat-10.* ~/tomcat
   ```

3. 启动 Tomcat：

   ```bash
   cd ~/tomcat/bin
   ./startup.sh
   ```

4. 停止 Tomcat：

   ```bash
   ./shutdown.sh
   ```

---

### 4. 验证安装

打开浏览器访问：

```
http://localhost:8080
```

此时应显示 Tomcat 欢迎页面。

---

### 5. （可选）添加环境变量

为支持在任何路径执行 `startup.sh`，请将以下内容添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
export CATALINA_HOME=~/tomcat
export PATH=$CATALINA_HOME/bin:$PATH
```

重新加载配置：

```bash
source ~/.zshrc
```

---

👉 至此，你已成功在 macOS 上本地运行 Tomcat。

需要继续了解 **如何在 macOS 上向 Tomcat 部署 WAR 文件** 吗？
