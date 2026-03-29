---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 连接微信指南
translated: true
type: note
---

将 **OpenClaw** 与 **WeChat**（亦称微信）结合使用，可以让您的个人微信账号成为 AI agent 的交互界面。基于最新的 2026 版本，主要有两种实现方式：**Official Plugin**（最简便）和 **Community Bridge**（适用于高级用户/服务器）。

---

## Method 1: The Official Plugin (推荐)
这是最快的方法（约耗时 5 分钟），通过扫描二维码即可支持个人微信账号。

### 1. Prerequisites
* **OpenClaw CLI:** 确保版本为最新（v2026.3.22 或更高）。
* **Node.js:** 已安装在您的机器上。
* **WeChat App:** 准备好手机以便扫码。

### 2. Installation Steps
在终端中运行以下命令：

* **Step A: One-Click Install**
    ```bash
    npx -y @tencent-weixin/openclaw-weixin-cli install
    ```
* **Step B: Login via QR Code**
    运行登录命令以在终端生成二维码：
    ```bash
    openclaw channels login --channel openclaw-weixin
    ```
    使用手机微信扫码并确认授权。
* **Step C: Restart the Gateway**
    ```bash
    openclaw gateway restart
    ```

### 3. Usage
一旦 Gateway 重启，您发送给自己的任何消息（或根据配置收到的消息）都将由 OpenClaw AI agent 处理。您可以要求它：
* “总结我的未读消息。”
* “提醒我下午 6 点去看望父母。”
* “为这段文字草拟一份专业的回复。”

---

## Method 2: Community Bridge (Docker Method)
如果您在 Linux 服务器上运行 OpenClaw，或者想要更精细的控制（例如“ClawBot”风格的集成），可以使用 Community Bridge。

### 1. Requirements
* **Docker Desktop** (>= 4.0)
* **OpenClaw Gateway** 已在运行。

### 2. Deployment
1.  **Clone the bridge repository:**
    ```bash
    git clone https://github.com/laolin5564/openclaw-wechat.git
    cd openclaw-wechat
    ```
2.  **Start the Protocol Service:**
    ```bash
    cd wechat-service
    ./start.sh
    ```
    这将启动包含 WeChat protocol、MySQL 和 Redis 的 Docker 容器。
3.  **Link to OpenClaw:**
    进入 bridge 文件夹并运行设置：
    ```bash
    cd ../bridge
    npm install
    npm run setup
    ```
    系统会提示您输入 **OpenClaw Gateway Token**（可在 `~/.openclaw/openclaw.json` 中找到）。
4.  **Scan and Chat:**
    终端将出现一个二维码。扫码以绑定您的账号。

---

## Key Configurations
为确保消息处理正确，请检查 `~/.openclaw/openclaw.json` 中的以下设置：

| Setting | Command to Set | Description |
| :--- | :--- | :--- |
| **Context Isolation** | `openclaw config set agents.mode per-channel-per-peer` | 防止不同的微信联系人查看到彼此的聊天历史。 |
| **Plugin Toggle** | `openclaw config set plugins.entries.openclaw-weixin.enabled true` | 确保官方插件已启用。 |

> [!TIP]
> **Safety Note:** 如果您使用的是个人账号，强烈建议开启 `per-channel-per-peer` 模式，这样 AI 就不会混淆您与家人、同事以及您个人备忘录之间的对话。

需要我帮您查找 **Gateway Token**，或者指导您为微信设置特定的 **Skills**（如自动排程或文档总结）吗？