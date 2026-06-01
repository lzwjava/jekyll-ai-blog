---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在AMD MI300X上设置NanoGPT
translated: true
type: note
---

以下是操作步骤：

1. 通过 SSH 登录到 root@129.212.187.36（AMD MI300X，Ubuntu）

2. 安装 HF CLI
   - `pip3 install -U --break-system-packages 'huggingface_hub[cli]'`
   - huggingface_hub 1.17.0

3. 从 HuggingFace 下载 lzwjava/zz
   - `hf download lzwjava/zz --local-dir /root/zz`
   - 37 个文件，424K（非 git 下载）

4. 为 GitHub 生成 SSH 密钥
   - ed25519，标签 `lzwjava-amd-devcloud`
   - 已添加至 GitHub

5. 克隆包含完整历史记录的 nanoGPT
   - `git clone git@github.com:lzwjava/nanoGPT.git`
   - 255 次提交，位于 /root/nanoGPT

6. 从 HF 重新克隆 zz 作为正规 git 仓库
   - 删除了非 git 的 `hf download` 版本
   - `git clone https://huggingface.co/lzwjava/zz`
   - 设置远程仓库：origin → GitHub（已归档），hf → HuggingFace（活跃）
   - 18 次提交，完整历史

7. 通过 `zed ssh://root@129.212.187.36//root/zz` 打开 Zed

8. 冒烟测试下载脚本
   - `plan_and_download_fineweb_gpt3_amd.py` — 运行正常，267 MB/s

9. 用户在 tmux 中运行完整下载
   - 18 个分片，39 GB，约 10.4B 个 FineWeb-Edu token
   - 完成

10. 安装分词依赖
    - tiktoken, numpy, pyarrow, tqdm

11. 冒烟测试分词脚本
    - `tokenize_fineweb_gpt3.py` — 运行正常，约 30-50M tok/s
    - 输出：uint16, GPT-2 BPE, EOT 前缀 ✓

当前状态：
  /root/nanoGPT   — nanoGPT 仓库（255 次提交）
  /root/zz        — 数据集仓库（18 次提交，39 GB parquet 数据）
  下一步：        — 分词为 .npy 分片，然后训练