---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ww：开发者生产力工具包
translated: true
type: note
---

## 这是 **`ww`** —— 一款提升开发者生产力的跨平台 CLI 工具包 🚀

这是一个基于 Python 的命令行工具（版本 0.1.0），堪称开发者的 **瑞士军刀**，并全面集成了 **基于 LLM 的智能** 功能。以下是其涵盖的功能：

### 核心能力

| 类别 | 功能说明 |
|----------|-------------|
| **🔄 Git** | AI 提交信息、压缩提交、强制推送、差异树、提交分类 |
| **🐙 GitHub** | 仓库列表、通知、星标仓库、粉丝管理、AI 提交生成 |
| **🖼️ 图像** | 截图、裁剪、压缩、背景去除、EXIF 扫描、图像生成 |
| **📄 PDF** | 将 PDF 转换为 Markdown/LaTeX、代码转 PDF、解析 Cloudflare Analytics PDF |
| **🌐 网页搜索** | 多引擎搜索（Tavily 等）并附带 AI 驱动结果 |
| **🔍 网络** | WiFi 扫描、IP/端口扫描、网络拓扑、DNS 查询、速度测试 |
| **💻 系统** | macOS/Linux 监控、进程管理、主机信息 |
| **📝 笔记** | 集成 Git 的笔记记录、日志条目、敏感数据脱敏 |
| **🗣️ 语音** | 使用 Whisper 进行转录并辅以 AI 优化 |
| **📊 Cloudflare** | Web 分析（页面浏览量、访问量）、区域管理 |
| **🛡️ Clash 代理** | 代理管理、速度测试、DNS 解析、WiFi 切换 |
| **🎓 教育** | 自考学位通知抓取并附带 AI 分类 |
| **🤖 LLM** | 模型对比、RAG 文档索引、OpenRouter 管理 |
| **🛠️ 其他** | Marp 演示文稿、Ghostty 终端控制、GitHub Actions 触发、Java/Maven 分析、Cloudflare 分析等等 |

### 技术栈

- **Python ≥ 3.11**，推荐使用 `uv` 作为包管理器
- 集成 **Google Gemini**、**OpenRouter**、**Whisper**、**Tavily**
- macOS 特有功能利用原生框架（Quartz、CoreWLAN、CoreText）
- 跨平台（macOS、Linux）

简而言之，这是一个 **个人开发者生产力利器**，可自动化从 git 工作流到网络诊断的各类操作，全部通过 `ww <group> <command>` 命令即可调用。
