---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Git与快照下载对比
translated: true
type: note
---

HuggingFace Hub 和 GitHub 有着根本性的不同：

**GitHub（`git pull`）** — 基于 git 历史记录操作。快进（fast-forward）意味着将分支指针向前移动。这是一种*合并*操作，会尊重提交谱系、分支以及工作树状态。仅处理发生变更的文件。

**HuggingFace Hub（`snapshot_download`）** — 并非执行 git pull。它从 HF 的存储 API 下载一份扁平的*快照*文件，并将其写入磁盘。这里没有合并、没有分支追踪、也没有提交历史感知。它更像是 `rsync` 或 `wget -r`。

因此，在你的 `zz` 仓库中发生的情况是：

1. **未跟踪的文件（logs/）** — 这些文件存在于你的 HF 仓库中，但不在你的本地 git 里。`snapshot_download` 只是将它们写入目录。它们显示为未跟踪，因为 git 发现了它不了解的新文件。

2. **已修改的文件（scripts/）** — `snapshot_download` 使用 HF 版本*覆盖*了本地文件。如果 HF 快照中包含这些脚本的旧版本/不同版本，它就会替换它们。Git 会看到差异。

3. **没有快进的概念** — HF 不知道你本地的 git 状态。它只是说“这是仓库中的文件，把它们写下来”。它不会进行差异比较、合并或询问。

这就是工作流程存在细微差异的原因：

- `git pull` = 智能三方合并，尊重历史
- `hf pull` = 从远程快照盲目覆盖文件

如果你想要与 HF 进行真正的 git 风格同步，你应该使用 `git clone https://huggingface.co/lzwjava/zz` — 实际上 HF 仓库底层也是 git 仓库。但 `snapshot_download`（即 `ww hf pull` 所使用的）是“原样下载所有内容”的方式，专门针对模型分发而非代码协作进行了优化。