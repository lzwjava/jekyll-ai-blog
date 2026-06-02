---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 顶级Mac性能与存储提升
translated: true
type: note
---

以下是按投资回报率排序的**当前可操作的高影响事项**：

---

### 最大收益

| 操作 | 释放空间 | 方法 |
|---|---|---|
| **清除 JetBrains 缓存** | ~7 GB | `rm -rf ~/Library/Caches/JetBrains/` |
| **Homebrew 清理** | ~3 GB | `brew cleanup --prune=all` |
| **pip 缓存清除** | ~2.4 GB | `pip cache purge` |
| **清除微信缓存** | ~5-10 GB | 微信设置 > 存储 > 清理 |
| **关闭 Vivaldi/Safari 标签页** | ~10 GB 内存 | 关闭不需要的页面 |
| **不使用时退出微信** | ~5-19 GB 内存 | 直接退出应用 |
| **退出闲置的 VSCode 项目** | ~15 GB 内存 | 关闭未使用的窗口 |
| **切换输入法**（搜狗→苹果自带） | ~3.5 GB 内存 | 系统设置 > 键盘 |

### 其他建议

- **Spotlight 索引** — 开机后 CPU 飙升至 250% 属于正常现象，等待 15 分钟即可。可在 Spotlight 隐私设置中排除 `node_modules/`、`~/Projects/`、`~/Library/Caches/` 等目录，长期保持快速。
- **48 GB 剩余空间** — 建议保留 >100 GB。最安全的清理方式：仅 JetBrains 缓存 + Homebrew + pip 即可释放约 12 GB。

---

需要我执行上述清理操作吗？我也可以推荐哪些内容可迁移到你的远程 RTX 4070 机器（编译、机器学习、重度开发），让这台笔记本保持精简，充当瘦客户端。
