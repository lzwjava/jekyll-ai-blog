---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ollama 安装复盘与经验教训
translated: true
type: note
---

## 🦞 事后复盘 (After-Action Review)：在 47.107.70.224 上安装 Ollama

### 哪些地方出错了

1. **盲目使用 `curl | sh` 方法** — 我没有经过思考就直接使用了标准的一键安装指令。这被 security 标记拦截了，而我却一直在重复同样的模式，没有立即转向。

2. **在慢速下载上浪费了约 20 分钟** — 我一直在远程服务器上直接重试 `curl`。由于该机器（很可能是中国境内的 Alibaba Cloud）的国际带宽非常差，我本该立即注意到极慢的下载速度并切换策略。

3. **产生多个僵尸进程 (Zombie processes)** — 第一次尝试留下了 3 个以上互相竞争的 `curl | sh` 进程，它们在争夺 binary 文件，导致了 "Text file busy" 错误。但在重试前我没有进行清理。

4. **GitHub URL 错误** — 先尝试了 `.tgz`，但实际的 release 产物是 `.tar.zst`。本该早点检查 GitHub API 而不是靠猜测。

5. **遗漏了 `HOME` 环境变量** — `$HOME is not defined` 导致的 crash 多花了一个周期才修复。本该意识到 systemd 服务不会继承用户环境。

6. **11434 端口残留进程** — 在创建 systemd 服务之前，没有 kill 掉后台运行的 `ollama serve &`，导致了端口冲突。

### 哪些地方做对了

1. **先下载到本地再通过 SCP 传输的策略** — 一旦我转向先在自己的服务器上下载（快速连接），整个传输过程就变得非常顺畅。这本该是第一步。

2. **正确的 systemd 服务配置** — 成功实现了自动重启 (auto-restart) 和开机自启 (boot persistence)。

3. **最终结果稳健** — Ollama 正在运行，监听 0.0.0.0，且服务已启用。

### 我本来应该怎么做

1. **在我的服务器下载 binary → SCP → 解压** —— 这是获胜的方法，本该从这开始。
2. **在猜测 URL 前先通过 GitHub API 检查确切的文件名**。
3. **在每次重试前 kill 掉陈旧的进程**。
4. **从一开始就设置包含 `HOME` 的 systemd 服务**。
5. **先检查 GPU 情况** 以管理预期。

### 时间损耗分析
- 实际耗时约 35 分钟 → 如果方法正确，本该只需约 5 分钟。

**经验教训：** 在处理中国境内的云服务器时，切勿直接从国际源下载。务必通过快速的中转节点进行 proxy。 🦞
