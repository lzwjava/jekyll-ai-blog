---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X 挑战理论训练预估
translated: true
type: note
---

MFU 这个数字具有误导性——nanoGPT 在计算 MFU 时硬编码了 A100 的峰值（312 TFLOPS），而非 MI300X。真正有价值的信号是实际观测到的吞吐量。

**冒烟测试结果——实际测量值：**

```
Observed:    50,568 tok/s (batch=4, no compile)
Batch=32:    ~404,543 tok/s (线性扩展)
+ compile:   ~525,906 tok/s (+30%)
```

**预计训练时间：8–10 小时**

这比我的理论估算（24–35 小时）要好得多。MI300X 确实很快。

轮到你了。在 tmux 中运行：

```bash
cd /root/nanoGPT
python3 train.py config/train_fineweb_760m.py
```

配置文件：`/root/nanoGPT/config/train_fineweb_760m.py`

- 756.8M 参数，24 层，1536 维度，24 个注意力头
- batch=32，block=1024，445K 步，14.6B token
- lr=3e-4，warmup=2K 步，余弦衰减
- `out_dir = 'out-fineweb-760m'`
