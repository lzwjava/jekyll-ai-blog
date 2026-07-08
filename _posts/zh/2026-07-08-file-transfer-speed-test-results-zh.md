---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 文件传输速度测试结果
translated: true
type: note
---

本机速度测试结果（12.5 MB/s 链路限制）：

| 方法 | 工作线程数 | 聚合速度 |
| ------ | ----------- | --------- |
| 顺序 wget | 1 | 14.0 MB/s |
| 并行 wget | 8 | 12.5 MB/s |
| hf_transfer + wget | 1 | 11.4 MB/s |

**瓶颈：** 机器到 HF 的链路已饱和，总速度约 12-14 MB/s。由于单流已占满整个管道，增加并行工作线程在此无帮助。

**但并行架构仍有价值，因为：**

- 在 **云 GPU 机器**（RunPod、Lambda 等）上，管道带宽为 100-1000 MB/s，并行工作线程可线性扩展
- 对慢速/重试文件具有弹性——一个超时不会阻塞其余任务
- 连接延迟开销由各工作线程分摊

**更新后的脚本位于 `codeparrot/download.py`：**

```bash
# 8 个并行工作线程
python3.11 download.py

# 16 个并行工作线程（适合云环境）
python3.11 download.py --workers 16

# 同时启用 hf_transfer
HF_HUB_ENABLE_HF_TRANSFER=1 python3.11 download.py --workers 16
```

运行完整管道：

```bash
bash codeparrot/run_pipeline.sh
```

对于您 192.168.1.36 的工作站，情况类似（家庭 ISP）。对于云环境（AMD Dev Cloud、RunPod），将 `--workers` 提升至 16-32 会实际发挥作用。
