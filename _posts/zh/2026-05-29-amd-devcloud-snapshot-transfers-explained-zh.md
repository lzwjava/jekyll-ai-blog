---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD DevCloud 快照传输说明
translated: true
type: note
---

**问题：** AMD DevCloud 中的 "transfer snapshot" 是什么意思，它与 DigitalOcean 有什么关系？

**回答：**

AMD Developer Cloud 运行在 DigitalOcean 之上——devcloud.amd.com 会重定向到 DigitalOcean，后者托管了 GPU Droplets。因此你看到的快照界面是由 DigitalOcean 的基础设施驱动的。

**Transfer Snapshot** 在 DigitalOcean（也就是支撑 AMD DevCloud 的平台）中有两层含义：

1. **转移到另一个团队/用户**：将 Droplet 快照移动到另一个 DigitalOcean 团队，或通过电子邮件将其转移给其他用户。转移快照后，该快照会从原团队中移除。适用于共享已配置的环境或迁移所有权。

2. **迁移到另一个区域**：将快照转移到另一个区域，以便随后在不同的数据中心创建新的 Droplet。这就是你将 MI300X Droplet 迁移到 DigitalOcean 不同地理区域的方式。

**快照为你带来的好处：**

快照允许你恢复 Droplet 的精确状态，无需重新运行配置，但会产生少量存储费用。在你的工作流程中：在配置好 ROCm、PyTorch 以及模型/数据集后拍摄快照。然后你可以销毁 Droplet 以停止计费，之后在约 2 分钟内从该快照启动一个新的 Droplet——所有配置都会被保留。

**实用工作流程：**
```bash
# 1. 配置你的 MI300X Droplet，训练模型等
# 2. AMD DevCloud UI → Snapshots → Take Snapshot
# 3. 销毁 Droplet（停止按小时计费）
# 4. 之后：从快照创建新 Droplet → 即时恢复
```

快照转移功能主要用于你想让其他人访问你配置好的环境，或者在区域之间进行迁移——对于个人开发来说不太常见，但在团队工作流程中很重要。

---

参考资料：

- [AMD Developer Cloud on DigitalOcean Architecture](https://www.phoronix.com/review/amd-developer-cloud)
- [DigitalOcean Transfer Snapshot Documentation](https://docs.digitalocean.com/products/snapshots/how-to/transfer/)
- [DigitalOcean Snapshot Migration Guide](https://docs.digitalocean.com/products/snapshots/how-to/migrate-droplets/)