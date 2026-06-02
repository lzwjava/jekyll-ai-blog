---
audio: false
date: 2025-09-09
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 管理Windows端口与进程
translated: true
type: note
---

在 Windows 系统中，你可以使用 `netstat` 查看哪些端口正在被监听（以及被哪个进程 PID 占用），然后通过 `taskkill` 管理或终止这些进程。这在调试后端项目（如 Java Spring Boot 应用、Redis 或 MySQL）时经常需要。具体操作如下：

---

### 1. 检查监听端口

以管理员身份运行 **命令提示符 (cmd)** 或 **PowerShell**：

```bash
netstat -ano | findstr LISTENING
```

* `-a` → 显示所有连接和监听端口
* `-n` → 以数字形式显示地址和端口
* `-o` → 包含 PID（进程 ID）

示例输出：

```
TCP    0.0.0.0:8080     0.0.0.0:0     监听中      12345
TCP    0.0.0.0:3306     0.0.0.0:0     监听中      6789
```

这里：

* 端口 `8080` 被 PID `12345` 占用（可能是你的 Spring Boot 应用）。
* 端口 `3306` 被 PID `6789` 占用（MySQL）。

---

### 2. 查找 PID 对应的进程

你可以将 PID 与进程名称匹配：

```bash
tasklist | findstr 12345
```

输出可能显示：

```
java.exe                  12345 控制台                    1     512,000 K
```

这意味着你的 Spring Boot 应用正在端口 8080 上运行。

---

### 3. 必要时终止进程

如果你想停止该进程：

```bash
taskkill /PID 12345 /F
```

* `/PID` → 指定进程 ID
* `/F` → 强制终止

---

### 4. 常见后端服务的典型端口

* **Spring Boot (Java 应用):** 8080、8081 等
* **MySQL:** 3306
* **Redis:** 6379
* **PostgreSQL:** 5432

因此，如果在 `netstat` 输出中看到这些端口，你就知道是哪个服务在运行。

---

👉 专业提示：你可以将这些命令组合成一个，直接查找特定端口（例如 8080）对应的进程：

```bash
netstat -ano | findstr :8080
```

然后获取 PID 并用 `tasklist` 检查。

---

需要我为你展示一个 **PowerShell 单行命令**，可以直接将端口映射到进程名称而无需单独使用 `tasklist` 检查吗？
