---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 修复Hugging Face下载缓慢问题
translated: true
type: note
---

这是通过代理下载大型HF数据集时的常见问题。以下因素组合会导致该问题：

* 大量数百MB的文件
* Python `requests` / `huggingface_hub` 库
* 本地HTTP代理（特别是Clash、V2Ray或tun2socks）

通常会导致极低的吞吐量或连接重置。

以下是最有效的解决方案。

---

## 1. **最佳解决方案：使用 `hf_transfer`**

Hugging Face提供了加速下载器，速度提升**10–50倍**且更稳定。

安装：

```bash
pip install hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1
```

重新运行命令。

仅此操作通常就能解决代理下载缓慢的问题。

---

## 2. 使用 `aria2c` 配合Hugging Face CLI（大文件下载最快）

如需手动下载：

```bash
pip install huggingface_hub[cli]
sudo apt install aria2
```

然后下载：

```bash
huggingface-cli download --repo-type dataset openwebtext --local-dir ./openwebtext --local-dir-use-symlinks False
```

HF CLI会自动使用aria2，它能更好地处理：

* 并行连接
* 断点续传
* 不稳定代理

效果远胜于 `requests`。

---

## 3. 修复本地代理缓慢：使用系统级SOCKS替代HTTP

如果当前使用类似配置：

```
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
```

若代理支持，请切换到SOCKS5：

```bash
export ALL_PROXY=socks5://127.0.0.1:7891
```

SOCKS在大文件流传输方面**稳定性显著提升**。

---

## 4. 对大文件禁用代理

若直连网络良好但代理导致减速：

```bash
unset HTTP_PROXY
unset HTTPS_PROXY
unset ALL_PROXY
```

重试操作。根据地区不同，部分HF服务器即使不通过代理也很快。

---

## 5. 使用HF镜像（中国大陆/台湾地区有时较慢）

可强制使用CDN：

```bash
export HF_ENDPOINT=https://hf-mirror.com
```

然后重新运行。
此举在某些地区会显著提升速度。

---

## 6. 恢复中断的下载

HF数据集缓存位置：

```
~/.cache/huggingface/datasets/
```

若有文件部分下载，HF会自动续传——无需从头开始。

---

## 7. 若仍缓慢：避免完整数据集，使用小规模切片

OpenWebText超过40GB。
可仅加载部分数据：

```python
from datasets import load_dataset
ds = load_dataset("openwebtext", split="train[:1%]")
```

---

## 快速建议

最快速+最简单的方案：

```bash
pip install hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1
python data/openwebtext_10k/prepare.py
```

应立即观察到下载速度跃升。

---

如果需要，我可以演示如何修改 `prepare.py` 来使用完全自定义的下载器，具备重试/退避和并行获取功能，确保您的流水线始终快速下载且永不卡顿。
