---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 查找并终止JMX端口进程
translated: true
type: note
---

明白了 — 您需要检查 Windows 上哪个 Java 程序在 `9091` 端口打开了 **JMX 远程代理**，并在必要时将其终止。以下是具体操作步骤：

---

### 1. 查找占用 9091 端口的进程

以管理员身份打开 **命令提示符**，运行：

```cmd
netstat -ano | findstr :9091
```

输出示例如下：

```
  TCP    0.0.0.0:9091    0.0.0.0:0    监听中     12345
```

* 最后一列（此处为 `12345`）即 **PID（进程标识符）**。

---

### 2. 根据 PID 确认对应程序

将 PID 映射至实际程序：

```cmd
tasklist /FI "PID eq 12345"
```

输出示例如下：

```
映像名称                       PID  会话名              内存使用
========================= ======== ================ ============
java.exe                    12345 Console           200,000 K
```

若确认为 Java 进程，可进一步查看详细信息：

```cmd
wmic process where processid=12345 get CommandLine
```

此命令将显示启动 JVM 的 **命令行参数** — 您会看到 JMX 相关参数（如 `-Dcom.sun.management.jmxremote.port=9091`），从而确认此为 JMX 远程代理。

---

### 3. 终止进程

确认可安全停止后，执行终止操作：

```cmd
taskkill /PID 12345 /F
```

* `/PID` 指定进程标识符
* `/F` 表示强制终止

---

### 4. 使用 PowerShell 的替代方案

若倾向使用 PowerShell，可运行：

```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 9091).OwningProcess
```

直接终止命令：

```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 9091).OwningProcess -Force
```

---

🔎 流程总结：

1. `netstat -ano | findstr :9091` → 获取 PID
2. `tasklist /FI "PID eq <PID>"` → 确认程序名
3. `wmic process where processid=<PID> get CommandLine` → 查看 JVM 参数
4. `taskkill /PID <PID> /F` → 终止进程

---

需要同时 **检查多个 JVM 的 JMX 代理端口** 吗（例如查看 9090、9999 等端口是否也有服务运行）？
