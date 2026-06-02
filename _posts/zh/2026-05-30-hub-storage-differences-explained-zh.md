---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hub存储差异详解
translated: true
type: note
---

很好的问题。让我从存储层开始解释。

## 核心区别：Git vs Git LFS vs Xet

**GitHub** 将所有内容存储在标准 Git 对象（packfile）中。Git 专为源代码设计——它能很好地压缩文本差异，但处理大型二进制文件时表现不佳。每个版本的二进制文件基本上都会被完整存储。一个 7GB 的模型文件有 10 个版本，服务器上就会占用约 70GB。

**Hugging Face Hub** 表面上是 Git，但对于大文件使用了**两种不同的后端**：

### 1. Git LFS（传统方案，仍为默认）

当你运行 `hf upload lzwjava/zz .` 时，对于大文件实际发生的过程如下：

```
你的机器                    HF Hub
───────────                     ──────
git commit (小文件)     ───>  标准 Git 仓库
                                (README.md, config.json 等)

LFS 指针文件            ───>  LFS batch API
(在 .gitattributes 中             将实际 blob 存储在
 追踪的大文件)                    对象存储中 (S3/GCS)
```

Git 仓库本身只包含**指针文件**——像这样的小文本存根：

```
version https://git-lfs.github.com/spec/v1
oid sha256:abc123...
size 7000000000
```

实际的模型权重存储在**对象存储**（S3/GCS）中。当你执行 `git clone` 或 `hf_hub_download` 时，LFS 的 smudge 过滤器会从对象存储中获取真实内容，而不是从 Git 中获取。

这就是为什么 HF 可以托管包含 100GB+ 模型文件的仓库——Git 从未看到实际的字节。

### 2. Xet（新方案，正在推广中）

HF 一直在构建一个名为 **Xet** 的新后端（基于内容定义的块划分，类似于 rsync/restic）。它不再将整个文件存储在对象存储中：

```
传统 LFS：     将整个 7GB 文件作为一个 blob 存储
Xet (CDC)：   将文件切分为约 64KB 的可变大小块，
              跨文件/版本去重这些块
```

这意味着，如果你微调一个模型且只有 5% 的权重发生改变，Xet 只会上传/存储修改过的块。对于迭代式的机器学习工作流来说，这是一个巨大的优势。你提到的 `hf_api.py` 在 `_upload_large_folder.py` 和整个下载路径中都引用了对 Xet 的支持。

## 架构对比

```
                    GitHub                    HuggingFace Hub
─────────────────────────────────────────────────────────────
协议                Git (smart HTTP)          Git (smart HTTP)
                                                + LFS batch API
                                                + Xet CAS API

大文件存储          Git LFS（可选，               Git LFS（默认）
                    按仓库选择加入）              + Xet（内容寻址
                                                  分块存储）

最大文件大小       建议 ~2GB                    支持 50GB+
                   （硬限制 ~100GB）

去重                无（仅 Git delta）          Xet：跨文件块去重

克隆/下载           git clone（拉取              hf_hub_download：
                    所有内容）                   选择性文件获取，
                                                  基于符号链接的缓存，
                                                  并行下载

仓库类型           只有“repo”                   models, datasets, spaces
                                                （每种有不同的元数据模式）

元数据             只有 README                  模型卡片（YAML 前置
                                                  信息），数据集标签，
                                                  库名称，指标，
                                                  许可证等

拉取模型权重       N/A（不为此设计）            一等特性：
                                                  snapshot_download()，
                                                  from_pretrained() 都从
                                                  Hub 拉取

网页托管           GitHub Pages                 Spaces（Gradio/Streamlit
                                                  应用，支持 GPU 托管）
```

## 为什么 GitHub 做不到（也不试图做）

GitHub 的价值在于**代码协作**——PR、议题、Actions CI/CD、代码审查。Git 的对象模型是为文本差异比较优化的。对 7B 参数的 `.safetensors` 文件执行 `git diff` 毫无意义。

HF Hub 的价值在于**模型分发**。整个存储层围绕“少量小配置文件 + 几个多 GB 且不常变更的二进制 blob”设计。`hf_hub_download` 中的选择性下载（只获取 `model-00002-of-00004.safetensors`，而不是整个仓库）在纯 Git 中是不可能实现的。

## 你的上传实际做了什么

```
Start hashing 36 files.      # 对每个文件哈希以检测变化
Finished hashing 36 files.   # 仅上传新的/有变化的文件
✓ Uploaded                   # 通过 HF API 推送提交
```

哈希步骤是 HF 实现增量上传的方式——它检查哪些文件已存在于 Hub 上（通过 SHA256），并跳过它们。这比 `git push` 更智能，后者会重新发送未变化的 LFS 对象。

对于 `zz`（你的 CLI 工具），仓库可能全是小文件，所以本质上就是一次普通的 git push。但如果你上传了一个 7GB 的 `.safetensors` 模型，它会透明地走 LFS/Xet 路径。
