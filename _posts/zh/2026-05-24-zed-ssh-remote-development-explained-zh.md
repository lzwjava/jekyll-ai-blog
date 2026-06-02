---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zed SSH远程开发详解
translated: true
type: note
---

**问题：** Zed 是否像 VS Code 的 Remote SSH 扩展一样支持远程 SSH 服务器？
**回答：**

是的，Zed 提供 SSH 远程开发支持，而且效果相当不错——在某些方面甚至比 VS Code 的 Remote SSH 更简洁。

## 工作原理

通过 SSH 进行编辑时，Zed 会通过 `ssh.exe` 运行一个轻量级的“远程服务器”进程，所有 I/O 操作都通过该进程路由。大多数功能都支持远程编辑：加载/保存文件、Git 集成、终端、任务、语言服务器和调试器。

UI 完全在本地运行（120fps GPU 渲染），但语言服务器、任务和终端在远程服务器上运行，以便充分利用云硬件资源。

## 快速开始

使用 `ctrl-cmd-shift-o`（macOS）或 `alt-ctrl-shift-o`（Linux）打开“远程项目”对话框。点击“连接新服务器”并输入 SSH 命令。Zed 会在远程主机上下载服务器二进制文件并自动启动。

对于简单情况，你也可以直接运行：
```
zed ssh://[user@]host[:port]/path
```

## 与 VS Code Remote SSH 的主要区别

| 特性 | Zed | VS Code |
|---|---|---|
| UI 渲染 | 本地（GPU，120fps） | 本地 |
| LSP 运行 | 远程 ✅ | 远程 ✅ |
| 服务器二进制文件 | 自动下载 | 基于扩展 |
| 配置来源 | 读取你的 `~/.ssh/config` | 相同 |
| ControlMaster 重用 | 支持（近期版本） | 无原生支持 |

Zed 最近进行了调整，可以重用现有的 SSH ControlMaster 会话，而无需再次提示输入凭证——如果你已经连接到 Ubuntu 工作站或 AMD Dev Cloud，这会非常方便。

## 注意事项

SSH 远程功能需要一个单一的二进制可执行文件，通过 SSH 与你本地机器上的 Zed 通信。它会自动安装在远程主机上，但在受限/离线环境中，需要手动预安装 `zed-remote-server`。

## 针对你的设置

要连接到你的 `192.168.1.36` 上配备 RTX 4070 的 Ubuntu 工作站，只需运行：

```bash
zed ssh://lzw@192.168.1.36/path/to/project
```

或者对于 AMD Dev Cloud（亚特兰大），使用相同的模式替换为你的云主机地址。语言服务器和 GPU 密集型进程都在远程运行，而 Zed UI 在你的 M2 Air 上保持流畅。

**参考资料：**

- [Zed 远程开发文档](https://zed.dev/docs/remote-development)
- [SSH 远程功能已到来 —— Zed 博客](https://zed.dev/blog/remote-development)
- [Zed for Windows（WSL/SSH 架构细节）](https://zed.dev/blog/zed-for-windows-is-here)
