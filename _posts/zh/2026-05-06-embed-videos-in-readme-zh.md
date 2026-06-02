---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在GitHub README中嵌入视频
translated: true
type: note
---

**问题：** 如何在 GitHub 的自述文件中正确显示/嵌入视频？

**回答：**

你当前的做法遇到的核心问题是：**GitHub 不会渲染指向 `raw.githubusercontent.com` 的 `<video>` 标签**，它只会显示一个损坏的播放器或什么都不显示。GitHub 只解析托管在其自有资产 CDN（`github.com/user-attachments/assets/...`）上的视频。

以下是可行的方法，按推荐程度从高到低排列：

---

## ✅ 方法 1：拖放上传（最佳且最简单）

这是官方支持的方式。在 GitHub 网页编辑器中打开你的自述文件进行编辑，然后将 `tot.mp4` 文件直接拖放到编辑器中。GitHub 会自动上传它并生成一个类似 `https://github.com/lzwjava/Tree_Of_Thought/assets/{id}/....mp4` 的 URL。

使用 `https://github.com/user-attachments/assets/${UUID}` 格式的 URL 是有效的，但 `https://github.com/${user}/${repo}/raw/main/some/path/demo.mp4` 对于视频嵌入来说无效。

**步骤：**

1. 前往你的 GitHub 仓库 → 点击铅笔图标 ✏️ 编辑 `README.md`
2. 将本地的 `tot.mp4` 文件拖拽到文本编辑器区域
3. 等待上传完成——GitHub 会插入一行类似这样的内容：

```markdown
https://github.com/lzwjava/Tree_Of_Thought/assets/XXXXX/XXXXXXXX.mp4
```

4. 将其包裹在 `<video>` 标签中，或直接使用：

```html
<video src="https://github.com/lzwjava/Tree_Of_Thought/assets/XXXXX/XXXXXXXX.mp4" controls width="100%"></video>
```

5. 提交并保存——视频播放器将渲染在你的自述文件中。

> **注意：** 免费版 GitHub 计划的文件大小限制为 10 MB，付费版为 100 MB。

---

## ✅ 方法 2：可点击缩略图（备用方案——无大小限制）

如果你的视频过大，可以使用链接到视频文件的缩略图：

```markdown
[![观看视频](https://raw.githubusercontent.com/lzwjava/Tree_Of_Thought/main/thumbnail.png)](https://raw.githubusercontent.com/lzwjava/Tree_Of_Thought/main/tot.mp4)
```

这使用 Markdown 创建了一个图片链接——点击缩略图会打开原始视频文件。你需要先将一个缩略图文件（例如 `thumbnail.jpg`）提交到仓库中。

---

## ❌ 为什么你当前的方法行不通

```html
<video src="https://raw.githubusercontent.com/lzwjava/Tree_Of_Thought/main/tot.mp4" controls width="100%"></video>
```

GitHub 的 Markdown 渲染不支持使用指向原始仓库文件路径的 `<video>` 标签直接嵌入视频——这是 GitHub 已知的限制。

---

## 总结表

| 方法 | 在自述文件中有效吗？ | 大小限制 |
|---|---|---|
| 拖放上传（GitHub CDN URL） | ✅ 是 | 10–100 MB |
| `raw.githubusercontent.com` 的 `<video>` 标签 | ❌ 否 | — |
| 可点击缩略图 → 原始链接 | ✅ 是（无自动播放） | 无限制 |
| YouTube 嵌入缩略图 | ✅ 是 | 无限制 |

**建议操作：** 使用方法 1——将 `tot.mp4` 文件拖放到 GitHub 网页编辑器中，以获取正确的 CDN 链接。

**参考链接：**

- [bobbyhadz.com - 如何将视频嵌入 GitHub README.md](https://bobbyhadz.com/blog/embed-video-into-github-readme-markdown)
- [GitHub 社区讨论 - Readme.md 视频不工作](https://github.com/orgs/community/discussions/19403)
- [amonxu.com - 如何将视频嵌入 GitHub README](https://amonxu.com/2024/05/23/en/2024-05-23-How-to-embed-a-video-into-GitHub-README/)
- [GeeksforGeeks - 如何将视频嵌入 GitHub README.md](https://www.geeksforgeeks.org/git/how-to-embed-a-video-into-github-readme-md/)
