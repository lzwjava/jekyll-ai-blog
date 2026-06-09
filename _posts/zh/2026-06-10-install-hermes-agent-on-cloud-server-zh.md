---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在云服务器上安装Hermes代理
translated: true
type: note
---

问题：我应该在 AMD 开发者云服务器上安装 Hermes Agent 用于 LLM 实验，还是将其保留在笔记本电脑上并通过 SSH 使用？

答案：对于在 AMD 开发者云实例上进行 LLM 训练和推理实验，你应**直接在云服务器上安装 Hermes Agent**（或将笔记本电脑上的 Hermes 实例配置为使用其原生的 **SSH 终端后端**）。

以下是为什么将 Hermes Agent 放在云服务器上或利用其原生远程执行能力是更优方案，相比于每次都手动从笔记本电脑 SSH：

### 1. 自主、长时间运行的实验

LLM 训练和微调需要时间。如果你在笔记本电脑上运行 Hermes Agent 并强制其每次操作都手动 SSH，一旦笔记本电脑休眠、失去 Wi-Fi 或断开连接，实验就会失败或停止。

* 直接在 AMD 服务器上安装 Hermes 可使其 7×24 小时运行。
* 你可以完全断开连接、合上笔记本电脑，并通过 Telegram、Discord 或 Slack 等消息平台远程与 agent 交互。

### 2. 原生多后端沙箱

Hermes Agent 原生支持 **6 种终端后端**，包括 **Local** 和 **SSH**。

* **如果你更喜欢在笔记本电脑上使用 Hermes Desktop GUI：** 你不再需要手动 SSH。你可以在笔记本电脑上安装 Hermes，将其后端配置为 **SSH**，并指向你的 AMD 云实例。Hermes 将自主管理 SSH 连接，直接在 GPU 集群上执行 bash 脚本、运行 Python 代码和读取文件。
* **如果你希望完全独立：** 通过 Docker 或标准安装直接在 AMD 服务器上运行 CLI 版本，这将为 Hermes 提供超快的本地执行速度，便于处理数据集、日志和模型检查点。

### 3. 训练循环集成与工具网关

Hermes Agent 具有持续学习循环，可将成功的代码模式、错误解决方案和命令保存为 markdown “技能”。如果 Hermes 存在于服务器上（或通过 SSH 后端原生管理服务器），它可以主动查看你的 AMD ROCm/PyTorch 日志，捕获 CUDA 内存不足错误，修改超参数，并自动重启训练循环，无需你作为中间人。

---

### 总结建议

| 方案 | 推荐度 | 最佳适用场景 |
| --- | --- | --- |
| **安装在 AMD 云上（本地/Docker）** | **强烈推荐** | 重度自动化、24/7 训练运行，以及通过 CLI 或移动聊天应用（Telegram/Slack）与服务器交互。 |
| **安装在笔记本电脑上，使用 Hermes SSH 后端** | **不错的替代方案** | 如果你更偏好使用 **Hermes Desktop App** 界面，同时让 agent 处理云 GPU 上的 SSH 繁重工作。 |
| **从笔记本电脑手动 SSH** | **不推荐** | 将自己束缚在终端上违背了自主 agent 的初衷；任何网络中断都会导致管道失败。 |

要在你的 AMD 云实例上开始使用，只需运行服务器安装脚本：

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup
```

参考链接：

* [Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs/)
* [Hermes Agent 官方新版 Desktop App 视频](https://www.youtube.com/watch?v=nb5ALoAGAbE)

该视频演示了原生 Hermes Desktop 应用程序界面，展示了 agent 如何管理持久环境、文件树和自动化任务。
