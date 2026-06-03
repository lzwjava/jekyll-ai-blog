---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 培训进度报告摘要
translated: true
type: note
---

运行良好。以下是摘要：

- 模型：286M参数（深度=12，维度=768）
- 吞吐量：约55,700 tok/秒（约1.17秒/步）
- 损失：10.40 → 7.25（前32步，预热阶段——损失快速下降，一切正常）
- 预计完成时间：约196分钟（约3.3小时）完成10K步
- 第0步的验证bpb：3.22
- VRAM：远低于12GB（device_batch_size=8没问题）
- GPU利用率：98%

一切看起来正常。预热期间损失平稳下降。一旦预热结束且学习率稳定，损失下降速度会减慢，然后在长时间训练阶段进一步下降。
