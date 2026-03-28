---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何停止远程 AI 进程
translated: true
type: note
---

要从您当前的笔记本电脑停止由 OpenClaw（或任何 AI agent）在远程机器（如 `192.168.1.36` 或 `47.107.70.224`）上启动的长时间运行的进程——特别是当 Web interface 无响应时——您有以下几种选择：

---

### **1. 通过 SSH 进入远程机器**
如果您拥有远程机器的 SSH 访问权限，可以登录并手动停止进程。

#### **步骤：**
1. **SSH 进入远程机器：**
   ```bash
   ssh user@192.168.1.36
   ```
   （请将 `user` 替换为实际的用户名。）

2. **查找进程：**
   使用 `ps`、`top` 或 `htop` 查找正在运行的进程：
   ```bash
   ps aux | grep ollama
   ```
   或者
   ```bash
   sudo systemctl status ollama
   ```

3. **停止进程：**
   - 如果它是 systemd service：
     ```bash
     sudo systemctl stop ollama
     ```
   - 如果它是普通进程，使用 `kill`：
     ```bash
     kill -9 <PID>
     ```
     （将 `<PID>` 替换为实际的 process ID。）

---

### **2. 使用 Systemd（如果适用）**
如果进程由 systemd 管理（如您的日志所示），您可以通过 SSH 远程停止它：
```bash
ssh user@192.168.1.36 "sudo systemctl stop ollama"
```

---

### **3. Web Interface 超时**
如果 Web interface 无响应，可能是由于：
- 进程消耗了所有资源。
- 崩溃或挂起。

在这种情况下，**SSH 是重新获得控制权的最佳选择**。

---

### **4. 通过脚本自动化（如果您有权限）**
如果您经常需要停止此类进程，可以在远程机器上创建一个脚本并通过 SSH 触发它：
```bash
ssh user@192.168.1.36 "/path/to/stop_script.sh"
```

---

### **5. Web Chat 的局限性**
如果您是问是否可以 **直接通过 Web chat 界面**（如 chatbot 或 OpenClaw 的 UI）停止进程：
- **不可以**，除非 Web interface 提供了内置的 “stop” 按钮或 API endpoint。
- 如果 UI 已冻结，您必须使用 SSH 或其他远程访问方法。

---

### **解决眼前的问题**
根据您的日志，问题在于：
> `Service is crash-looping — Ollama panics with $HOME is not defined.`

#### **解决方案：**
编辑 Ollama 的 systemd service 文件并设置 `HOME` 环境变量：
```bash
sudo systemctl edit ollama
```
添加：
```
[Service]
Environment="HOME=/home/your_user"
```
然后重启：
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

**如果您在执行这些步骤时需要任何帮助，请告诉我！**
您是否需要针对特定部分的详细步骤指南？