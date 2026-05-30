---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过删除旧文件释放磁盘空间
translated: true
type: note
---

这是你的磁盘情况。共有460GB磁盘，仅剩**2.9GB可用**（已使用81%）。以下是占用空间最大的部分及清理命令：

## 主要占用项

```
  27 GB   ~/projects/warp/target          (Rust 构建产物)
  19 GB   /opt/homebrew                   (Homebrew 包)
  12 GB   ~/Library/JetBrains             (缓存 + 应用支持)
   8 GB   Docker 容器数据                 （未运行，可安全清除）
   8 GB   Bodhi-AI/target + node_modules
   7 GB   ~/.npm                          (npm 缓存)
   7 GB   ~/Library/Caches/JetBrains
   3.7 GB ~/Library/Caches/Homebrew
   3 GB   其他 node_modules
   2.5 GB ~/Library/Caches/pip
   2.8 GB ~/.hermes
   1.8 GB ~/.cargo
   1.3 GB LarkShell 缓存
   1 GB   Playwright 浏览器
```

## 快速清理 — 现在即可安全删除

```bash
# 1. Rust target 目录（收益最大 — 34GB 以上）
rm -rf ~/projects/warp/target
rm -rf ~/projects/Bodhi-AI/target
rm -rf ~/projects/zenith/bamboo/target

# 2. npm 缓存 (7 GB)
npm cache clean --force

# 3. Docker (8 GB，Docker 甚至未运行)
rm -rf ~/Library/Containers/com.docker.docker

# 4. Homebrew 缓存 (3.7 GB)
brew cleanup --prune=all

# 5. JetBrains 缓存 (7 GB，不会影响项目)
rm -rf ~/Library/Caches/JetBrains

# 6. pip 缓存 (2.5 GB)
pip cache purge

# 7. Playwright 浏览器 (1 GB，仅当你不需要时)
npx playwright uninstall --all

# 8. Homebrew 下载缓存残留
rm -f ~/Library/Caches/Homebrew/downloads/*.dmg
```

## 中等优先级 — 请先检查

```bash
# JetBrains 应用支持 (5.4 GB) — 仅在你不需要旧版 IDE 时删除
du -sh ~/Library/Application\ Support/JetBrains/*

# 未使用的 Homebrew 包（仅 llvm 就占用 1.7 GB）
brew leaves           # 列出手动安装的包
brew uninstall <pkg>  # 移除不使用的包
```

## 监控 — 如果磁盘持续增长

```bash
# 查看当前正在写入的内容
sudo fs_usage -w -f disk 2>/dev/null | head -50

# 或查找一小时内修改过的文件
find ~ -type f -mmin -60 -size +10M 2>/dev/null

# 快速检查总使用量
du -sh ~/projects ~/Library ~/.npm ~/.cargo ~/.hermes 2>/dev/null
```

仅 Rust 的 `target` 目录就能释放约 34GB。这是你最大的收益——下次 `cargo build` 会重新构建，但鉴于只剩 2.9GB 可用空间，这是值得的。需要我帮你运行其中任何命令吗？