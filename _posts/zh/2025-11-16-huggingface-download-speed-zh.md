---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Hugging Face下载速度优化方案
translated: true
type: note
---

您遇到的问题在中国大陆（尤其是广州等南方地区）从Hugging Face下载大文件时非常典型。

### 为何不使用代理时速度极慢（约200-300 KB/s）

- 即使您使用**hf-mirror.com**（HF与01.AI运营的官方中国镜像站），FineWeb的实际大型parquet文件**并未在中国境内缓存**
- hf-mirror.com仅将您重定向至全球CDN（现通过AWS美东一区的xet-bridge传输）
- 从广州直连时：您的流量需经过国际网关（中国电信/联通/移动骨干网→美国AWS），大文件下载会遭遇严重限流或QoS限制。2GB文件很容易降至<500KB/s，有时甚至低至100KB/s

### 为何启用Clash代理后速度飙升（常达20-100 MB/s）

- 您的Clash很可能使用了香港、台湾、日本、新加坡或韩国节点（广州用户常见配置）
- 这些节点具备：
  - 与AWS美东一区（或HF使用的Cloudflare）直连或优质网络连接
  - 不受防火墙出境流量限制
  - 更高带宽保障
- 因此即使经过代理"绕行"，实际传输路径仍远快于中国大陆直连国际网络

### 核心结论

从广州直连（即使通过hf-mirror.com）→ 因实际存储仍在美国，且2025年中国至美国大文件带宽状况依然堪忧，导致速度缓慢
Clash代理（港/台/日/新节点）→ 因这些节点与美国AWS具有极佳连通性，速度飞快

### 推荐解决方案（按速度从高到低排序）

1. **持续使用Clash（或v2rayN/Surge等）配合低延迟港/台/日节点** — 当前在中国大陆下载FineWeb、RedPajama、The Stack等数据集的最快方式

2. 使用**HF中国官方加速端点**（2024-2025年多数用户无需代理即可使用）：

   ```bash
   export HF_ENDPOINT=https://hf-mirror.com
   ```

   随后直接使用huggingface-cli或datasets库（非wget）。因HF在2025年已将更多数据分片缓存于阿里云/腾讯云，目前国内用户实测速度达50-200MB/s

3. 使用**FastGit + hugger**或**openi/pkulaw镜像站**（部分分片已国内缓存）：
   示例：

   ```bash
   pip install hugger
   hugger download HuggingFaceFW/fineweb --revision main --include "CC-MAIN-2013-20/*.parquet"
   ```

4. 保持wget + hf-mirror.com组合，但强制通过Clash代理传输（即您当前方案）

### 广州用户高速下载FineWeb分片的一行命令

```bash
# 设置Clash HTTP代理（默认端口常为7890）
export https_proxy=http://127.0.0.1:7890

# 使用aria2（比wget更快且支持断点续传）
aria2c -x16 -s16 -k1M "https://hf-mirror.com/datasets/HuggingFaceFW/fineweb/resolve/main/data/CC-MAIN-2013-20/000_00000.parquet"
```

根据代理节点质量，您将轻松获得30-100MB/s的下载速度。

最终结论：在2025年的中国大陆，下载Hugging Face上>1GB文件时，使用港/台/日代理仍几乎总是比直连更快——即使通过hf-mirror.com访问。这就是当前中国国际带宽的现实状况。
