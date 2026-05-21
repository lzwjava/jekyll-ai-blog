---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 标签杀手：最终仓库结构
translated: true
type: note
---

完成。推送 `3d8090e` → `master`。

最终仓库结构位于 https://github.com/lzwjava/TabsKiller：

```
README.md           ← 英文，同时支持 Chrome + Safari
README-CN.md        ← 中文
safari-tab-killer.png   ← Safari 截图（664 KB）
safari-tab-killer.mp4   ← Safari 演示视频（664 KB）
chrome-tab-killer/      ← Chrome 扩展（以未打包方式加载）
├── manifest.json
├── popup.html / popup.js / background.js
├── css/ img/ js/
└── ...
safari-tab-killer/      ← Safari Web 扩展 + Xcode 项目
├── manifest.json
├── TabsKiller.xcodeproj/
├── TabsKiller/ (Swift 应用)
└── ...
```

两个 README 都涵盖了功能、各浏览器的安装方法以及背后的故事。Safari 部分内嵌了截图并提供了 mp4 演示视频。Chrome 则链接到 Web Store，并显示了版本徽章。