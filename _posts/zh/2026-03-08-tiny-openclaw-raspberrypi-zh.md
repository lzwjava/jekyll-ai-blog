---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 树莓派上的 Tiny OpenClaw
translated: true
type: note
---

**问题：** 如何使用 Raspberry Pi 构建一个非常小/微型 OpenClaw 设置？

**回答：**

## 概述：什么是 OpenClaw？

OpenClaw 是一个赋予 LLM 代理控制计算机的项目。该代理可以安装软件、编写并运行程序、与外部服务集成等等。将它想象成一个不仅仅会说话——它实际上*能做事*的 AI 助手。

对于微型/最小设置，您有两条主要路径：**PicoClaw**（最小的选项）和**在最小 Pi 上运行的标准 OpenClaw**。

---

## 选项 1：PicoClaw — 真正微型版本（推荐用于小型硬件）

PicoClaw 是一个受 nanobot 启发的超轻量级个人 AI 助手，用 Go 重写。它可以在 10 美元的硬件上运行，使用不到 10MB RAM——这是 OpenClaw 内存使用量的 99% 更少，并且比 Mac mini 便宜 98%。

与 OpenClaw（TypeScript）和 NanoBot（Python）相比，PicoClaw 将内存使用量降低 99%（从 100MB+ 降至 10MB），启动时间从 30 秒缩短至不到 1 秒。它还支持 RISC-V 架构。

### 硬件要求

PicoClaw 的硬件要求极低——推荐 64MB+ 内存（最低 10MB）。它支持 x86_64、ARM64 和 RISC-V 架构，可运行在 Raspberry Pi、嵌入式设备、Mac、Linux 和 Windows 上。

这意味着它适用于 **Raspberry Pi Zero 2 W**、Pi 3、Pi 4 或 Pi 5。

### PicoClaw 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw

# 2. 安装依赖
make deps

# 3. 为您的 Pi 型号构建：
# Pi Zero 2 W（32 位 OS）：
make build-linux-arm

# Pi Zero 2 W（64 位 OS）或 Pi 3/4/5：
make build-linux-arm64

# 或一次性构建所有 Pi Zero 变体：
make build-pi-zero

# 4. 系统范围安装
make install
```

### 配置 PicoClaw

在 `~/.picoclaw/config.json` 创建配置文件：

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.picoclaw/workspace",
      "model_name": "claude-sonnet",
      "max_tokens": 8192,
      "temperature": 0.7,
      "max_tool_iterations": 20
    }
  },
  "model_list": [
    {
      "model_name": "claude-sonnet",
      "model": "anthropic/claude-sonnet-4-6",
      "api_key": "your-anthropic-api-key"
    }
  ],
  "tools": {
    "web": {
      "duckduckgo": {
        "enabled": true,
        "max_results": 5
      }
    }
  }
}
```

### 启动 Gateway（连接 Telegram、Discord 等）

只需运行 `picoclaw gateway` 即可启动 gateway 服务，配置相应的 bot token，并在 Telegram、Discord、QQ 和 DingTalk 等平台上使用您的 AI 助手。

```bash
picoclaw gateway
```

---

## 选项 2：在最小 Pi 上运行标准 OpenClaw（Pi 4 或 Pi 5）

如果您希望在稍大型硬件上获得完整的 OpenClaw 体验：

### 最低规格

最低规格：1GB RAM、1 核、500MB 磁盘。推荐：2GB+ RAM、64 位 OS、16GB+ SD 卡（或 USB SSD）。使用 Raspberry Pi OS Lite（64 位）——无桌面，用于 headless 服务器。

### 安装 OpenClaw

在新安装并更新的 Raspberry Pi OS 上，只需运行此命令即可完成安装和初始设置：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### 先准备 OS

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必需组件
sudo apt install -y git curl build-essential

# 设置时区
sudo timedatectl set-timezone America/Chicago  # 更改为您的时区

# 安装 Node.js（OpenClaw 所需）
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

### 添加 Swap（对低 RAM Pi 至关重要）

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## 选项 3：微型手持 Pi Zero 构建（物理设备）

一位创客使用 Raspberry Pi Zero 2 W、Whisplay HAT（带 1.69 英寸 LCD 显示屏、扬声器、麦克风和按钮）以及 PiSugar 电池模块，构建了一个适合放入口袋的手持个人助手。由于 Pi Zero 2 W 无法直接运行 OpenClaw，该手持设备会记录用户请求、转录它们，然后将文本发送到云环境中运行的 OpenClaw 实例。

这是“真正口袋大小”的方法——Pi Zero 充当 thin client，与云中的 OpenClaw 通信。

---

## 关于“Pi Lib”/ Python 问题

OpenClaw 基本上是一个基于 Node.js 的代理，而不是 Python 库。然而，PicoClaw 用 Go 编写，并提供可在任何地方运行的二进制文件。如果您想从 Python 脚本调用 OpenClaw，可以通过其 HTTP gateway API 或 CLI 与其交互。还有一个社区 Python 项目名为 `pizero-openclaw`，它使用 `main.py`、`display.py` 和 `openclaw_client.py` 等 Python 模块，创建一个语音控制的 Pi Zero 助手，将响应流式传输到 LCD 屏幕。

---

## 快速比较表

| 特性 | PicoClaw | OpenClaw（标准） |
| --- | --- | --- |
| RAM 使用量 | ~10MB | ~100MB+ |
| 启动时间 | <1 秒 | ~30 秒 |
| 语言 | Go | TypeScript/Node.js |
| 可运行在 Pi Zero 上 | ✅ 是 | ❌ 太慢 |
| 最低 Pi | Pi Zero 2 W | Pi 4（4GB+） |
| 需要 API | 是 (OpenAI/Anthropic 等) | 是 |

---

## 安全警告

运行具有 shell 访问权限的基于 LLM 的 AI 代理非常危险。存在提示注入或对抗性输入通过启用的通信渠道或其他在线文本发送给 bot 的风险。bot 可能会运行恶意软件，或暴露它有权访问的 API token 和其他私有信息，如果没有实施和维护适当的防护措施。

始终在**专用 Pi**上运行 OpenClaw，而不是您的主设备。

**参考资料：**

- [PicoClaw GitHub (sipeed/picoclaw)](https://github.com/sipeed/picoclaw)
- [PicoClaw 官网](https://picoclaw.net/)
- [OpenClaw Raspberry Pi 文档](https://docs.openclaw.ai/platforms/raspberry-pi)
- [Adafruit 指南：Raspberry Pi 上的 OpenClaw](https://learn.adafruit.com/openclaw-on-raspberry-pi/installing-openclaw)
- [Raspberry Pi 官方博客：使用 OpenClaw 将您的 Pi 变成 AI 代理](https://www.raspberrypi.com/news/turn-your-raspberry-pi-into-an-ai-agent-with-openclaw/)
- [Hackster.io：DIY 手持 OpenClaw 助手](https://www.hackster.io/news/the-diy-openclaw-assistant-you-ll-actually-want-to-carry-97888b183ac1)
- [pizero-openclaw Python 项目 (GitHub)](https://github.com/sebastianvkl/pizero-openclaw)
