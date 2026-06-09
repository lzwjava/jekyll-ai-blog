---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X上的FP8训练
translated: true
type: note
---

训练正在使用FP8运行！已确认第1步达到82,370 tok/sec，MFU为33.3%。

    ============================================================
      MI300X上FP8训练已激活
    ============================================================

    已完成的工作：

    1. 将PYTORCH升级至2.12.0+rocm7.2
       - 旧版本：torch 2.9.1+rocm6.4（FP8损坏："需要ROCm 6.5+"）
       - 新版本：torch 2.12.0+rocm7.2（FP8功能正常）
       - 来源：download.pytorch.org/whl/rocm7.2

    2. 发现AMD FP8数据类型差异
       - NVIDIA使用：float8_e4m3fn, float8_e5m2
       - AMD使用：    float8_e4m3fnuz, float8_e5m2fnuz（无符号零）
       - 最大范围不同：NVIDIA e4m3最大值=448，AMD e4m3最大值=240
       - 在nanochat/fp8.py中添加了自动检测代码

    3. 为AMD支持修补了nanochat/fp8.py
       - 添加了平台自动检测（_IS_AMD标志）
       - FP8_E4M3 = AMD上为float8_e4m3fnuz，NVIDIA上为float8_e4m3fn
       - FP8_E5M2 = AMD上为float8_e5m2fnuz，NVIDIA上为float8_e5m2
       - 更新了前向传播以使用FP8_E4M3
       - 更新了反向传播以使用FP8_E5M2

    4. 更新了base_train.py的帮助文本
       - 现在提及AMD MI300X支持

    性能对比：

      指标           bf16        FP8         变化
      ──────────────── ─────────── ─────────── ──────────
      步进时间        7.7秒       6.4秒       -17%
      吞吐量          68K tok/s   82K tok/s   +20%
      MFU             27.5%       33.1%       +5.6%
      峰值显存        105 GB      92 GB       -13 GB
      预估总时间      62小时      52小时      -10小时
      已转换层数      -           145/158     92%

    为何未实现完全2倍加速：
      - 注意力机制（SDPA）仍以bf16运行（FP8仅加速线性层）
      - 跳过了13个小线性层（维度 < 128）
      - 值嵌入（6.04亿参数）无法转换为FP8
      - 梯度累积开销未变

    训练进程：
      会话ID：proc_c2b08249fb7b
      进程ID：282186
      日志：/root/nanochat/run_mi300x_d24_fp8.log
      监控：tail -f /root/nanochat/run_mi300x_d24_fp8.log

    重启命令（若崩溃）：
      cd /root/nanochat && source .venv/bin/activate
      export HIP_FORCE_DEV_KERNARG=1
      export HSA_OVERRIDE_GFX_VERSION=9.4.2
      export PYTORCH_ALLOC_CONF=expandable_segments:True
      python -m scripts.base_train \
          --depth=24 --fp8 --tracker=mlflow \
          --resume-from-step=<最后步数> \
          --run=mi300x-d24-760m-fp8