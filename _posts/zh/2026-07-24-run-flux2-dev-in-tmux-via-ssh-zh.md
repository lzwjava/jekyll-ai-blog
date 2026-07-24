---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过SSH在tmux中运行FLUX.2-dev
translated: true
type: note
---

一切就绪。现在通过 SSH 连接并在 **tmux 会话** 中运行（这样即使断开连接，进程也会继续运行）：

```bash
ssh -p 31145 root@36.150.116.206

# 启动 tmux
tmux new -s flux

# 激活环境并运行
source /root/flux_env/bin/activate
python3 /root/run_flux.py
```

下载大小约为 **35GB**，需要一些时间（根据镜像速度，约 15–30 分钟）。脚本将执行以下操作：
1. ✅ 从 HuggingFace 镜像下载 FLUX.2-dev
2. ✅ 将模型加载到你的 AMD GPU（48GB 显存）
3. ✅ 生成一张测试图像（`test_flux.png`）

要 **分离** tmux 并让其在后台运行：按 `Ctrl+B，然后 D`
稍后要 **重新连接**：运行 `tmux attach -t flux`