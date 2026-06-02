---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 磁盘空间限制macOS交换增长
translated: true
type: note
---

坏消息——**你无法在 macOS 上手动增加交换空间**。内核会自动管理交换，并且没有任何设置（GUI 或 CLI）可以更改交换大小。

你当前的情况如下：

```
Swap:   2048 MB total, 1222 MB used (encrypted)
Disk:   460 GB total, 425 GB used, only 12 GB FREE (98% full!)
RAM:    16 GB
Compressor: ~16.5 GB being compressed
```

**真正的问题是磁盘几乎满了。** 只剩 12 GB 可用空间，即使 macOS 想扩展交换也做不到。系统内存严重不足——大量使用内存压缩（超过 100 万页）且交换已耗尽，说明系统正在严重颠簸。

你可以采取以下措施：

1. **释放磁盘空间** —— 这是最有效的方法。你需要至少 10-15% 的可用空间（约 45-70 GB）才能保证健康的交换及交换文件扩展。一些快速清理方法：

```
# 查看哪些文件占用了空间
du -sh ~/Library/Caches/*
du -sh ~/Downloads
# 清空废纸篓
rm -rf ~/.Trash/*
# 清除 Xcode 衍生数据（如有）
rm -rf ~/Library/Developer/Xcode/DerivedData
# 清除 Homebrew 缓存
brew cleanup --prune=all
# 清除 pip/uv 缓存
pip cache purge
uv cache prune
```

2. **关闭占用内存较多的应用** —— Safari 开了很多标签页、Electron 应用（Slack、VS Code、Discord）通常是常见元凶。在 `Activity Monitor -> Memory` 中按内存使用量排序查看。

3. **如果你长期需要更多内存空间** —— M2 Air 采用的是统一内存，无法升级。16 GB 是物理上限。你的选择：
   - 使用更轻量的应用（例如用 Arc 替换 Chrome 等）
   - 同时打开更少的应用/标签页
   - 对于 GPU/ML 相关的工作，使用你的工作站（RTX 4070，62 GB 内存）——那正是它的用途

总结：清理磁盘空间。460 GB 磁盘只剩 12 GB 可用才是瓶颈，而不是交换配置的问题。
