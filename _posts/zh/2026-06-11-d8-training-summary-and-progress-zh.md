---
audio: false
generated: true
image: false
lang: zh
layout: post
title: d8 培训总结与进展
translated: true
type: note
---

```
d8 训练总结
===================

模型：
  架构：depth=8, dim=512, heads=4, head_dim=128, seq=1024
  参数量：125,829,354（约1.26亿）
  每次token的FLOPs：273M（比d4多3.8倍）

训练配置：
  步数：5,000
  批量大小：4,096 tokens/步
  总token数：20,480,000（约2000万）
  追踪器：MLflow (http://192.168.1.36:5000)

进度（前3步）：
  第0步：loss 10.398 | 46 tok/sec | 耗时 88s
  第1步：loss 10.397 | 53 tok/sec | 耗时 77s
  第2步：loss 10.395 | 61 tok/sec | 耗时 67s
  第0步的Val bpb：3.209

稳态估计：
  ~60 tok/sec，~68s/步
  5000步 × 68s = 340,000s ≈ 94小时 ≈ 4天

与d4的对比：
  d4：  3700万参数，115 tok/sec，18s/步
  d8：  1.26亿参数，60 tok/sec，68s/步
  速度比：115/60 = 1.9倍（根据FLOPs预期为3.8倍，但torch.compile在更大模型上分摊了开销）

正在运行的会话：
  1.36：tmux dist-master（训练）+ tmux mlflow（UI在端口5000）
  1.47：tmux dist-worker

MLflow UI：http://192.168.1.36:5000
```