---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用第二台电脑运行 OpenClaw
translated: true
type: note
---

**问题：** 我应该在主电脑还是第二台电脑上安装 OpenClaw？

**答案：**

**安装在你的第二台（专用/辅助）电脑上。** 这是 OpenClaw 官方文档和更广泛社区的强烈推荐。以下是详细原因分解：

---

### 🔒 安全原因（最重要）

OpenClaw 是一个强大的自托管 AI 助手，能够执行管理日历、浏览网页和运行终端命令等任务。它**不应在你的个人电脑上运行**，因为赋予 AI 代理高权限系统访问会带来重大安全风险。

运行具有 shell 访问权限和文件权限的代理会创建真实的攻击面。OpenClaw 可以从网页或群聊读取不受信任的文本。

OpenClaw 可以运行触及真实数据的 skills/tools。最近的报道强调了“skills”生态系统的真实安全风险——因此从隔离环境（Docker 或专用服务器）开始，并仅白名单你能控制的内容。

---

### 🖥️ 硬件要求

你的第二台电脑只需满足以下最低要求：

一台现代笔记本电脑配备 8 GB RAM 通常足以运行云模型和轻量自动化。对于更重的负载，16 GB 或更多是更安全的基准。强烈推荐使用 SSD 存储，以加快日志、缓存访问和模型下载速度。

全新 OpenClaw 安装大约需要 500 MB 磁盘空间（包括 node_modules）。推荐至少保留 5 GB 可用磁盘空间以留出扩展空间。OpenClaw 本身在空闲时大约使用 200–400 MB RAM。

---

### ⚙️ 常开优势

安装在专用第二台电脑上，还意味着它可以 24/7 持续运行，而不会干扰你的主工作流程。`--install-daemon` 标志会将 OpenClaw 注册为后台服务——Linux 上为 systemd，macOS 上为 launchd。这确保代理能在重启后存活并保持“常开”状态。

---

### ✅ 总结

| 因素 | 主电脑 ❌ | 第二台电脑 ✅ |
| --- | --- | --- |
| 安全 | 高风险——完全系统访问 | 隔离，更安全 |
| 性能 | 与日常工作竞争 | 专用资源 |
| 常开 | 不便 | 理想 |
| 若被入侵 | 个人数据面临风险 | 损害被限制 |

如果你的第二台电脑性能较低（例如旧笔记本），只要使用基于云的 LLM 而非本地模型，它仍然能正常工作。对于运行本地模型，更高的 RAM 和不错的 CPU/GPU 更重要。

---

**参考资料：**

- [OpenClaw Security & DigitalOcean Deployment Guide](https://www.digitalocean.com/community/tutorials/how-to-run-openclaw)
- [OpenClaw System Requirements](https://openclawdoc.com/docs/getting-started/requirements/)
- [How to Install OpenClaw 2026 - Medium](https://medium.com/@guljabeen222/how-to-install-openclaw-2026-the-complete-step-by-step-guide-516b74c163b9)
- [OpenClaw Hardware Requirements](https://clawbot.ai/openclaw-system-requirements.html)
- [OpenClaw Install Docs](https://docs.openclaw.ai/install)
