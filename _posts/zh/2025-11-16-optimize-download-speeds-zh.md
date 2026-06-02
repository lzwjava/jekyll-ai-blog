---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 优化Hugging Face下载速度
translated: true
type: note
---

您当前的下载请求正访问 Hugging Face 主端点 (`huggingface.co`)，该服务主要托管在欧美数据中心。从广州经台湾代理转发会产生相似的延迟问题：约200-300毫秒往返延迟，大文件还可能被限速（每个 Parquet 分片约500MB–1GB）。您遇到的 302 重定向很可能指向 CloudFront CDN 边缘节点，但可能并非亚洲地区最优节点，导致降速（例如 1–5 MB/s）。

要匹配维基媒体下载的 20–60 MB/s 速度，请采用以下优化方案——优先选择对亚洲网络友好的选项。所有方案均保留您的 Clash/台湾代理配置。

### 1. **切换至 HF 镜像站（中国/台湾地区最快——推荐）**
   HF 镜像站 (`hf-mirror.com`) 是社区运营的东亚优化 CDN（通过清华等国内网络代理）。它完整镜像所有 HF 数据集，包括 FineWeb 的 Parquet 文件。通过台湾代理下载可达 30–80 MB/s。

   更新您的脚本：
   ```bash
   #!/bin/bash
   # wget_fineweb_1.sh (速度优化版)
   mkdir -p fineweb_test_dump
   cd fineweb_test_dump
   echo "正在通过 HF 镜像站下载 FineWeb 分片（亚洲地区加速）..."

   # 将 huggingface.co 替换为 hf-mirror.com
   wget -c "https://hf-mirror.com/datasets/HuggingFaceFW/fineweb/resolve/main/data/CC-MAIN-2013-20/000_00000.parquet?download=true"

   echo "完成！分片大小：约500MB–1GB"
   echo "更多分片请循环下载，例如：000_00001.parquet 等"
   echo "Python 加载方式：from datasets import load_dataset; ds = load_dataset('HuggingFaceFW/fineweb', name='CC-MAIN-2013-20', split='train', streaming=True)"
   ```

   运行：`./scripts/train/wget_fineweb_1.sh`
   - 若镜像站延迟（罕见情况），可回退官方地址：`https://huggingface.co/datasets/...`（但需配合第2条速度优化技巧）

### 2. **启用 hf_transfer 加速（适用于所有 HF 下载——断点续传速度提升100倍）**
   Hugging Face 官方推出的 Rust 工具，支持并行/多线程下载。具备自动重试机制，使用更多连接数，优质链路下速度可超 500 MB/s。可通过 `wget` 间接使用或通过 Python 直接调用（如果脚本使用 `huggingface_hub`）。

   安装（一次性操作，通过 pip——您的环境已具备）：
   ```bash
   pip install hf_transfer
   export HF_HUB_ENABLE_HF_TRANSFER=1
   ```

   重新运行原始脚本。该工具会加速底层对 HF URL 的 `wget` 调用。
   - 专业建议：若需完整数据集流式传输（无需完整下载），请在管道中使用 Python：
     ```python
     from datasets import load_dataset
     import os
     os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'  # 导入前启用
     ds = load_dataset("HuggingFaceFW/fineweb", name="CC-MAIN-2013-20", split="train", streaming=True)
     for example in ds.take(1000):  # 实时流式处理
         print(example)
     ```
     若设置 `HF_ENDPOINT=https://hf-mirror.com`，将通过镜像站延迟加载分片

### 3. **Clash 规则调优（若允许——极速直连）**
   若代理配置允许绕过 HF 或路由至香港/新加坡节点，可为 `huggingface.co` / `hf-mirror.com` 添加直连/国内路由规则。在 `clash.yaml` 中：
   ```
   rules:
     - DOMAIN-SUFFIX,hf-mirror.com,DIRECT  # 或您的国内镜像节点
     - DOMAIN-SUFFIX,huggingface.co,DIRECT
   ```
   重启 Clash 后下载。配合第1方案可通过清华镜像达到 50–100+ MB/s

### 速度匹配原理说明
- 维基媒体：重定向器自动选择亚洲节点（日本/韩国/新加坡）→ 低延迟
- HF：默认欧美节点 → 高延迟；镜像站 + 传输加速可切换至亚洲优化节点

建议先测试单个分片——若速度仍不理想，可通过 `curl -I https://hf-mirror.com/...` 检查响应头（应显示亚洲 CDN）。对于完整的 15TB FineWeb 数据集，建议通过 `datasets` 库流式传输以避免下载数百 GB 数据。若速度未显著提升请随时联系！
