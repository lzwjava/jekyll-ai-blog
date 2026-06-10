---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MPS服务器烟雾测试通过
translated: true
type: note
---

服务器已在 MPS 上启动。现在进行冒烟测试——一次聊天补全：

冒烟测试通过——正在关闭服务器。

nanochat 在这台笔记本上运行正常。总结：

- **命令：** `uv run python -m scripts.chat_web --source base --port 8000`（从仓库根目录运行）  
- 现有的 `.venv` 可通过 `uv run` 正常工作，自动检测到 torch 2.9.1 并启用 **MPS**（Apple GPU）加速  
- 本地仅存在基础 `d4` 检查点（无 SFT/RL 检查点），故使用 `--source base`——若默认使用 `--source sft` 则会失败  
- 冒烟测试通过：`/health` 返回就绪状态，`/chat/completions` 流式输出 token。输出内容为乱码（如“attention Place Francis species…”），这符合预期——d4 是未经指令微调的小型基础模型  
- 随后已关闭服务器（退出码 144 仅为 pkill 所致，并非错误）

PyCharm 调试方法：将运行配置设为由模块 `scripts.chat_web` 启动，参数为 `--source base --port 8000`，工作目录为仓库根目录，解释器选择 `.venv`。若希望使用更简单的单进程进行单步调试，CLI 替代方案为 [chat_cli.py](scripts/chat_cli.py)（`python -m scripts.chat_cli -i base`）。