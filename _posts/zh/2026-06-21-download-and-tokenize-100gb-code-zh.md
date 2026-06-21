---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 下载并分词100GB代码
translated: true
type: note
---

Wget 运行结果：28秒下载273MB（约10 MB/秒）。100GB预计需要约3小时。

两个脚本已就绪并测试完成。汇总信息如下：

================================================================
在 /mnt/data/zz/ 中创建的文件
================================================================

/mnt/data/zz/scripts/download/download_github_code.py

- 从HuggingFace下载约100GB的代码parquet分片数据
- 支持断点续传（跳过已下载文件）
- 输出路径：/mnt/data/zz/datasets/github-code/*.parquet

/mnt/data/zz/scripts/extract/tokenize_github_code.py

- 将parquet文件分词并转换为nanoGPT二进制分片（.npy格式）
- 使用GPT-2 BPE分词器，每分片包含1亿个token
- 输出路径：/mnt/data/zz/datasets/github-code-tok/

================================================================
请在TMUX中按顺序执行（每次运行一个）
================================================================

步骤1 — 下载（约3小时）：

  python3.11 /mnt/data/zz/scripts/download/download_github_code.py

步骤2 — 分词（约1小时）：

  python3.11 /mnt/data/zz/scripts/extract/tokenize_github_code.py

================================================================
备注说明
================================================================

- 数据集包含1126个分片，每个约285MB，约含10万份代码文件
- 100GB数据约等于350个分片，约1290亿个token（远超训练760M模型所需）
- 数据列包括：代码内容、仓库名称、文件路径、许可证、文件大小（涵盖30种编程语言）
- 已下载并验证一个测试分片可正常使用
