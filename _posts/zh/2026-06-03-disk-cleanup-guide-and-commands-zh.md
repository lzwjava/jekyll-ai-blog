---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 磁盘清理指南与命令
translated: true
type: note
---

好的，以下是完整的现状说明。你的磁盘已使用 94%（实际可用仅 900MB，而非 12GB——那部分包含可清理空间）。

**空间大户（按大小排序）：**

```
 类别                        大小    处理建议
 ─────────────────────────────────────────────────────────────
 ~/.cache/huggingface/       21 GB   你下载的模型——可安全清理
 ~/projects/lzwjava.github.io 58 GB  巨大！检查是否有大型媒体文件或旧文章
 ~/Library/Containers/       37 GB   微信 19GB，Docker 8GB，QQ 4.5GB
 ~/.cache/ (总计)           31 GB   Hugging Face 21GB + torch 4.6GB + pre-commit 3GB + uv 1.3GB
 ~/Library/Caches/           22 GB   JetBrains 7.1GB，Homebrew 3.7GB，pip 2.6GB
 ~/Library/Application Sup.  24 GB   JetBrains 5.4GB，nomic.ai 3.5GB，飞书 2GB
 ~/.npm/                     7.2 GB  旧的 npm 缓存
 ~/.cache/torch/             4.6 GB  PyTorch hub 模型
 ~/Library/Developer/        3.8 GB  CoreSimulator 3.3GB
```

**快速清理（现在可安全删除，约 40+ GB）：**

```
# 1. HuggingFace 缓存（21 GB）——按需可重新下载
huggingface-cli scan-cache
huggingface-cli delete-cache

# 2. npm 缓存（7.2 GB）
npm cache clean --force

# 3. Homebrew 缓存（3.7 GB）
brew cleanup --prune=all

# 4. pip 缓存（2.6 GB）
pip3 cache purge

# 5. pre-commit 缓存（3 GB）
pre-commit clean

# 6. PyTorch hub 缓存（4.6 GB）——先检查再删除
ls ~/.cache/torch/hub/
rm -rf ~/.cache/torch/hub/*

# 7. JetBrains 缓存（7.1 GB）
rm -rf ~/Library/Caches/JetBrains/*

# 8. uv 缓存（1.3 GB）
uv cache prune
```

**更大规模清理（需要你确认）：**

```
# 微信（19 GB！）——打开微信设置 → 存储 → 清理
# 这是除 Hugging Face 缓存之外最易获得空间的单项

# Docker（8 GB）——如果在 Air 上不用 Docker：
docker system prune -a --volumes

# lzwjava.github.io（58 GB）——里面有什么？
du -sh ~/projects/lzwjava.github.io/*/ | sort -rh | head
# 很可能是大图片、视频或构建产物
```

需要我帮你运行安全清理命令（上面第 1-8 项）吗？这样可以释放约 40+ GB 空间。至于微信和博客仓库，我需要你来做决定。
