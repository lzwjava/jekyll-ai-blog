---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 迁移模型和Containerd数据
translated: true
type: note
---

&1  43.1s

╭─ ⚕ Hermes ──────────────────────────────────────────────────────────────────────────────────────────╮
    模型已复制（约37G）。现在进行交换并移动 containerd 数据。
╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
  ┊ 💻 准备终端…
  💻 ssh root@129.212.178.103 " # 交换：删除原始文件，将模型符号链接到卷 rm -rf /root/llama.cpp/models ln -s /mnt/volume_atl1_1780280110689/llama-models /root/llama.cpp/models ls -la /root/llama.cpp/models echo '===' # 现在移动 containerd 数据（59G） echo '=== 停止 containerd ===' systemctl stop containerd sleep 2 echo '=== 移动 containerd 数据 ===' rsync -a --progress /var/lib/containerd/ /mnt/volume_atl1_1780280110689/containerd-data/ " 2>&1  (06m13s)

 ⚕ mimo-v2.5-pro │ 96.9K/1M │ [█░░░░░░░░░] 9% │ 35m │ ⏱ 9m 13s
───────────────────────────────────────────────────────────────────
