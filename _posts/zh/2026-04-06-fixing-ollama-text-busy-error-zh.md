---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Ollama文本文件忙错误
translated: true
type: note
---

问题：Ollama安装出现了什么情况？如何修复“text file busy”错误以使Ollama正常运行？

回答：

“text file busy”错误（`ETXTBSY`）表示操作系统**已将二进制文件内存映射或正在被运行进程占用**，导致无法直接覆盖写入。这通常发生在以下情况：

- 崩溃的进程或僵尸进程仍保持文件打开状态
- systemd正尝试循环重启服务
- 部分安装导致二进制文件处于锁定状态

## 分步修复指南

### 1. 停止所有占用二进制文件的进程

```bash
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo pkill -9 ollama
sudo fuser -k /usr/local/bin/ollama   # 强制释放所有打开的文件句柄
```

### 2. 确认无进程占用文件

```bash
sudo lsof /usr/local/bin/ollama
# 应返回空结果
```

### 3. 删除损坏的二进制文件（不要直接覆盖，先删除）

```bash
sudo rm -f /usr/local/bin/ollama
```

即使覆盖写入失败，删除（解除链接）操作仍可执行，因为`rm`删除的是**目录条目**而非文件数据。任何仍持有文件打开状态的进程会保持其引用直到进程退出。

### 4. 重新全新安装Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sudo sh
```

若网络较慢可手动安装：

```bash
# 先下载至临时位置
curl -L https://ollama.com/download/ollama-linux-amd64 -o /tmp/ollama-new
sudo install -m 755 /tmp/ollama-new /usr/local/bin/ollama
```

### 5. 重新启用并启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

### 6. 验证服务监听状态

```bash
curl http://localhost:11434/api/tags
```

---

## 为何出现`status=203`（EXEC执行失败）？

systemd错误代码203表示二进制文件存在以下情况之一：

- 在预期路径**不存在**
- **无可执行权限**（权限错误）
- **缺少共享库**（`ldd`命令可显示损坏的依赖项）
- **架构不匹配**（例如在x86系统运行ARM二进制文件）

重新安装后，应在启动服务前执行`ldd /usr/local/bin/ollama`确认所有库文件正确解析。

参考资源：

- [Ollama Linux安装指南](https://ollama.com/download/linux)
- [理解systemd退出码203](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)
- [Linux ETXTBSY错误说明](https://man7.org/linux/man-pages/man2/open.2.html)
