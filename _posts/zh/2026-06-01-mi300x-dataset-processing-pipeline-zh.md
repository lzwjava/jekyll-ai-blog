---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X 数据集处理流水线
translated: true
type: note
---

全部完成。以下是摘要：

服务器：root@129.212.187.36 (MI300X, Ubuntu)
已安装：huggingface_hub 1.17.0（包含 `hf` 命令行工具）
已下载：lzwjava/zz → /root/zz (424K, 37 个文件)

内容：
  scripts/download/   — FineWeb/Wikimedia 下载脚本（含中国镜像 hf-mirror）
  scripts/extract/    — Parquet 提取、GPT-2 BPE 分词
  scripts/analysis/   — 训练时长、指标评估
  scripts/deepseek/   — DeepSeek-V2-Lite 推理（4-bit，12GB VRAM）
  logs/               — 训练日志（fineweb、openweb、do_fineweb、gen1/2）
  datasets/           — 数据集存储占位
  requirements.txt    — Python 依赖

HF token 已用于下载。该仓库是您的数据集处理 + 训练流程工具包 — 可直接在该 MI300X 机器上使用。
