---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC文件输出质量修复
translated: true
type: note
---

输出现在是连贯的SEC文件文本，包含真实财务数字和正确结构。以下是问题所在及修复内容：

== 根本原因 ==

  server.py 中的两个问题导致输出质量低于 nanoGPT 原生版本：

  1. SEC_SYSTEM 前缀——"以下是 SEC EDGAR 文件摘录..."
     被添加到每个提示前。模型在训练时并未见过此前缀，
     因此导致上下文混乱，产生重复/不连贯的输出。

  2. top_p=0.9 采样——nanoGPT 使用 top_k=200（保留前200个token，
     其余设为负无穷）。在124M模型上使用 top_p=0.9（核采样）
     效果更差——过多概率质量泄露到了低概率token。

== 修复 ==

  已更新 server.py：

- 移除了 SEC_SYSTEM 前缀——提示直接原样输入模型
- 从 top_p=0.9 切换为 top_k=200（与 nanoGPT sample.py 一致）
- 默认温度：0.7 → 0.8（与 nanoGPT 一致）

== 对比 ==

  修复前（top_p + SEC 前缀）：
    "我们的主要业务是我们的主要执行办公室，位于加利福尼亚州旧金山，
    以及旧金山，加利福尼亚州..."

  修复后（top_k=200，无前缀）：
    "$7,878,832 ... $8,798,871 ... 下表汇总了公司归属于非控制性权益的
    税前收入（亏损）变动... ASC 815，套期保值活动"

== 备注 ==

  nanoGPT 原生模型（ckpt.pt + model.py）输出的质量仍略优于
  HF transformers 版本——很可能是由于权重转换（词表从50304截断到50257，
  添加了零偏置）。但差距已大幅缩小。若希望进一步优化，可将 ckpt.pt + model.py
  上传至 RunPod，并使用原生模型类而非 transformers。
