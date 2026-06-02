---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 下载部分OpenWebText数据集
translated: true
type: note
---

啊，明白了——你想继续使用 **Hugging Face CLI** 但只获取一小部分数据。问题是：CLI 的设计初衷是下载**完整文件**而非片段。OpenWebText 被分割成 21 个 `.tar` 子集文件；如果使用 CLI，它会下载完整的压缩包，因此无法在不下载大文件的情况下精确获取「1%」的数据。

以下是可行的解决方案：

---

### 1. 仅下载部分文件

不下载全部 21 个文件，只选择少量压缩包：

```bash
huggingface-cli download \
  --repo-type dataset openwebtext/subsets/urlsf_subset00.tar \
  --local-dir ./openwebtext
huggingface-cli download \
  --repo-type dataset openwebtext/subsets/urlsf_subset01.tar \
  --local-dir ./openwebtext
```

* 每个压缩包约 625MB，下载 1-2 个相当于数据集的 1-2%
* 可自由选择子集，Hugging Face 不要求按顺序下载

---

### 2. 按需解压文件

下载完成后：

```bash
cd ./openwebtext
tar -xvf urlsf_subset00.tar
tar -xvf urlsf_subset01.tar
```

随后可仅处理这些子集中的部分文档

---

### 3. 可选：结合 HF Transfer 加速

提升 CLI 下载速度：

```bash
pip install hf_transfer
export HF_HUB_ENABLE_HF_TRANSFER=1
```

重新执行 CLI 命令后下载速度将显著提升

---

需要我编写一个**通过 CLI 自动选取约 1% OpenWebText 数据的精简命令脚本**吗？这样您就无需手动选择压缩包了。是否需要我实现这个功能？
