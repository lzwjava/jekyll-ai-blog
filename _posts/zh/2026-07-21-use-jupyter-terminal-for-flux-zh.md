---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Jupyter终端运行FLUX
translated: true
type: note
---

仍然是**权限被拒绝** —— 端口31090指向的是另一个实例的SSH，不是我们的。我们的密钥仅在端口31154（已关闭）上被授权。

**您的选项：**

1. **使用Jupyter终端**（已经可用）—— 直接运行FLUX.1-dev
2. **从AMD云控制台重启空间** —— 这应能重新映射端口31154
3. **将您的密钥添加到端口31090的SSH上** —— 但您需要访问该实例的权限

Jupyter是最快的途径。要在此处启动FLUX.1-dev吗？
