---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 火炬编译导致监控延迟
translated: true
type: note
---

问题：为什么训练监控在检查训练是否开始前要等待这么长时间（15秒→30秒→60秒→120秒）？

回答：

**torch.compile冷启动编译对于depth=12的模型很慢。**

当你运行第一个迭代时：
1. PyTorch 在 GPU 上编译前向/反向计算图（这是 JIT 编译的开销）
2. depth=12 是 768 维模型——比你之前测试的 depth=4 更大
3. 在你的 RTX 4070 上 torch.compile 冷启动：通常需要 60–120 秒

监控脚本采取保守策略——在轮询日志前增加休眠时间，让编译完成。这样虽然安全，但对迭代来说很慢。

**更快的替代方案：**

```bash
# 选项1：实时查看 GPU 实际活动（即时反馈）
watch -n 1 'nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader'

# 选项2：持续追踪日志（编译开始后即可生效）
tail -f /mnt/data/nanochat/train.log

# 选项3：激进轮询（每5秒检查一次，而不是休眠120秒）
for i in {1..20}; do tail -3 /mnt/data/nanochat/train.log && sleep 5; done

# 选项4：跳过轮询，直接连接到 tmux
tmux attach -t train
```

**加速迭代的方法：**

- 下次运行时设置 `--torch-compile=0`，如果编译开销影响你的开发体验
- 或者使用 `torch._dynamo.config.suppress_errors = True` 优雅处理边界情况
- 如果训练稳定性无需编译也能保障，编译只是优化手段——暂时跳过即可

14分钟时显示6%的进度，说明编译耗时大约90–120秒，随后训练启动较慢（需要预热）。到第1000步后你会看到实际吞吐量。

你的实际目标是什么——是需要快速获得编译反馈，还是追求最佳训练速度？