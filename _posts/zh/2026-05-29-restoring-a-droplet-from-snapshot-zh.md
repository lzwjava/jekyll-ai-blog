---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从快照恢复Droplet
translated: true
type: note
---

**问题：**“恢复 Droplet (restore droplet)”是什么意思？

**回答：**

“恢复 Droplet”是指使用快照将 Droplet 恢复到较早的时间点，这在恢复意外删除的文件或回退到已知正常的 Droplet 以从意外的配置更改中恢复时非常有用。

**主要区别：**

| 操作 | 具体行为 | 使用场景 |
| ----------- | ------------- | ----------- |
| **恢复 Droplet** | 用备份/快照中的先前状态完全替换正在运行的 Droplet。恢复期间 Droplet 会关闭，然后自动重新开启。 | 你犯了错误，想要撤销自快照以来的所有更改 |
| **创建 Droplet** | 从快照启动一个*新的*独立 Droplet | 你想要一份旧状态的副本，同时不丢失当前状态 |

**⚠️ 重要注意事项：**

目前无法撤销从备份恢复 Droplet 的操作。一旦恢复，快照之后的所有内容都将丢失。因此，如果你恢复到昨天的快照，今天所做的任何工作都将永久丢失。

**对于你的 AMD DevCloud 工作流程：**

只有在以下情况下才应使用恢复：

- 意外破坏了 ROCm/PyTorch 环境设置，想回退
- 想要还原错误的配置更改

通常情况下，你只需销毁 Droplet（停止付费），然后从快照创建一个新的即可。这样更干净，因为可以保持当前状态不变。

---

参考文档：

- [DigitalOcean 从快照创建/恢复](https://docs.digitalocean.com/products/snapshots/how-to/create-and-restore-droplets/)
- [DigitalOcean 从备份恢复](https://docs.digitalocean.com/products/backups/how-to/create-and-restore/)
