---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自动化MacBook备份流程
translated: true
type: note
---

一切就绪。以下是摘要：

    ========================================================================
      准备就绪
    ========================================================================

    脚本位于：MacBook (192.168.1.49) 上的 ~/backup.sh
    同时备份在：本机 (192.168.1.36) 的 /mnt/data/wuhuarong/backup.sh

    功能说明：
      使用 SSH 密钥认证（已配置） + rsync 将 MacBook 备份到本机的
      /mnt/data/wuhuarong/macbook-backup/ 目录。

      第一阶段 - 关键数据：SSH 密钥、git 配置、shell 配置、历史记录
      第二阶段 - 项目：~/Projects（27GB，最大块）
      第三阶段 - 个人文件：桌面、文档、下载、个人资料、照片整理
      第四阶段 - 应用数据：Joplin、OpenClaw、微信、Docker、Maven、令牌
      第五阶段 - 清单：生成包含所有文件大小的 MANIFEST.txt

    如何运行（在 MacBook 上）：
      bash ~/backup.sh

      主要耗时在 ~/Projects（27GB），其余数据较小（总计 < 6GB）。

    磁盘空间：/mnt/data 上有 1.1TB 可用空间，完全没问题。

    备份完成后即可安装 Ubuntu。备份将安全存放在本机
    /mnt/data/wuhuarong/macbook-backup/ 目录中。
