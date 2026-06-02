---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connecting OpenClaw with WeChat Guide
translated: false
type: note
---

Setting up **OpenClaw** with **WeChat** (also known as Weixin) allows you to use your personal WeChat account as an interface for an AI agent. Based on the latest 2026 releases, there are two primary ways to do this: the **Official Plugin** (easiest) and the **Community Bridge** (for advanced users/servers).

---

## Method 1: The Official Plugin (Recommended)
This is the fastest method (takes about 5 minutes) and supports personal WeChat accounts by scanning a QR code.

### 1. Prerequisites
* **OpenClaw CLI:** Ensure you have the latest version (v2026.3.22 or higher).
* **Node.js:** Installed on your machine.
* **WeChat App:** Have your phone ready to scan.

### 2. Installation Steps
Run the following commands in your terminal:

* **Step A: One-Click Install**
    ```bash
    npx -y @tencent-weixin/openclaw-weixin-cli install
    ```
* **Step B: Login via QR Code**
    Run the login command to generate a QR code in your terminal:
    ```bash
    openclaw channels login --channel openclaw-weixin
    ```
    Scan the code with your phone's WeChat app and confirm authorization.
* **Step C: Restart the Gateway**
    ```bash
    openclaw gateway restart
    ```

### 3. Usage
Once the gateway is restarted, any message you send to your own account (or that the account receives, depending on your config) will be processed by the OpenClaw AI agent. You can ask it to:
* "Summarize my unread messages."
* "Remind me to visit my parents at 6 PM."
* "Draft a professional reply to this text."

---

## Method 2: Community Bridge (Docker Method)
If you are running OpenClaw on a Linux server or want more granular control (like "ClawBot" style integration), you can use the community bridge.

### 1. Requirements
* **Docker Desktop** (>= 4.0)
* **OpenClaw Gateway** already running.

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
    This launches Docker containers for the WeChat protocol, MySQL, and Redis.
3.  **Link to OpenClaw:**
    Navigate to the bridge folder and run the setup:
    ```bash
    cd ../bridge
    npm install
    npm run setup
    ```
    You will be prompted for your **OpenClaw Gateway Token** (found in `~/.openclaw/openclaw.json`).
4.  **Scan and Chat:**
    A QR code will appear. Scan it to link your account.

---

## Key Configurations
To ensure your messages are handled correctly, check these settings in your `~/.openclaw/openclaw.json`:

| Setting | Command to Set | Description |
| :--- | :--- | :--- |
| **Context Isolation** | `openclaw config set agents.mode per-channel-per-peer` | Prevents different WeChat contacts from seeing each other's chat history. |
| **Plugin Toggle** | `openclaw config set plugins.entries.openclaw-weixin.enabled true` | Ensures the official plugin is active. |

> [!TIP]
> **Safety Note:** If you are using a personal account, it is highly recommended to use the `per-channel-per-peer` mode so the AI doesn't mix up conversations between your wife, your colleagues, and your own notes.

Would you like me to help you find your **Gateway Token** or guide you through setting up specific **Skills** for WeChat, like automated scheduling or document summarization?
