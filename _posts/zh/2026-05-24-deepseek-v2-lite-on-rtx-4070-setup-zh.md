---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek V2 Lite在RTX 4070上的设置
translated: true
type: note
---

================================================================
  DeepSeek-V2-Lite-Chat 在 RTX 4070 上的完整部署报告
================================================================

目标
----

在你的 RTX 4070（12GB 显存）上运行 DeepSeek 模型。
原版 DeepSeek-V4 代码位于 /mnt/data/deepseek-v4-inference，针对 671B+ 参数模型设计，需要 8 块 H100 GPU —— 在你的硬件上不可行。因此我们改用 DeepSeek-V2-Lite-Chat：采用相同的 MLA/MoE 架构，总参数量 16B（每 token 激活 2.4B 参数）。

步骤 1 — 从 git 拉取 ~/projects/ww
--------------------------------

从 github.com:lzwjava/ww 拉取最新代码。获得一次大更新：
140 个文件变更，新增 +21,275 行。新增模块涵盖 agents、tests、weather、machine info、hermes config、image EXIF、GitHub 管理等。

步骤 2 — 安装依赖
------------------------------

  python3.11 -m pip install --user bitsandbytes accelerate

  结果：
    bitsandbytes 0.49.2  — 4-bit NF4 量化
    accelerate 1.13.0    — device_map="auto" 实现多 GPU / CPU 卸载

  已安装：
    torch 2.6.0, transformers 4.48.3, safetensors 0.5.2

步骤 3 — 下载模型
------------------------

  模型：deepseek-ai/DeepSeek-V2-Lite-Chat
  目标路径：/mnt/data/models/DeepSeek-V2-Lite-Chat/

  首先尝试 HF 镜像站 (hf-mirror.com) 以加速下载 —— 失败，报错
  LocalEntryNotFoundError。降级为直接连接 HuggingFace。

  下载在后台运行，耗时约 35 分钟，总量 30GB：
    - 4 个 safetensor 分片（8.1GB x3 + 5.3GB x1）
    - 加上 tokenizer、config、modeling code（约 15 个小文件）
    - 速度：稳定约 1 GB/min

  下载脚本：
    from huggingface_hub import snapshot_download
    snapshot_download(
        'deepseek-ai/DeepSeek-V2-Lite-Chat',
        local_dir='/mnt/data/models/DeepSeek-V2-Lite-Chat'
    )

步骤 4 — 推理脚本
--------------------------

  编写 /mnt/data/deepseek-v4-inference/run_lite.py，包含：
    - 通过 BitsAndBytesConfig 实现 4-bit NF4 量化
    - 双重量化以进一步节省显存
    - bfloat16 计算数据类型
    - device_map="auto" 自动分配 GPU 资源
    - 交互式聊天模式与单次提示模式
    - CLI 参数：-p "prompt", -n max_tokens

步骤 5 — 修复：缺少 Python.h
--------------------------------

  首次运行失败 —— triton（bitsandbytes 的依赖）尝试编译 C 代码，需要 python3.11 对应的 Python.h，但系统中只安装了 python3.12-dev。

  修复：将 python3.12 的头文件软链接为 python3.11：
    sudo ln -sf /usr/include/python3.12 /usr/include/python3.11

  此举可行，因为 C API 兼容性足以满足 triton 的简单编译。修复后模型成功加载并运行。

步骤 6 — 测试运行
------------------

  命令：
    python3.11 run_lite.py -p "Hello! Who are you?"

  结果：
    加载时间：~2.5 分钟（4 个分片，每个约 37 秒）
    GPU 显存占用：9.5 GB（可用 11.6 GB）
    响应："I am an AI language model, here to assist you
              with information, questions, or tasks you have."

最终状态
-----------

  模型：      /mnt/data/models/DeepSeek-V2-Lite-Chat/（磁盘占用 30GB）
  脚本：      /mnt/data/deepseek-v4-inference/run_lite.py
  显存占用：  9.5 GB / 11.6 GB（82%）
  量化方式：  4-bit NF4 双重量化
  速度：      ~2.5 分钟加载，之后推理速度较快

使用方法
----------

  交互式聊天：
    python3.11 /mnt/data/deepseek-v4-inference/run_lite.py

  单次提示：
    python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "Explain quantum computing"

  生成更长输出：
    python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "Write a poem" -n 1024

与原始评估相比的变化
------------------------------------------

  原始代码：DeepSeek-V4（671B+ 参数，需要 8 块 H100）
  当前运行：DeepSeek-V2-Lite-Chat（16B 参数，1 块 RTX 4070）

同一架构家族（MLA + MoE），仅按硬件能力缩放到合适尺寸。相比 671B 模型会损失部分能力，但你能在本地实际运行它
================================================================

想尝试交互模式或调整任何设置吗？
