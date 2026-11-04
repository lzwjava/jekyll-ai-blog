---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 卡片设置完成预览
translated: true
type: note
---

明白了——从现在开始我会用英文回复。

先回顾一下当前进度：`ww card` 已完全配置好并提交，包含：

- **头像提取**：从你的照片中提取（macOS Vision 人脸检测）→ `card_output/avatar.jpg`
- **双语卡片**：`ww card --lang en`（仅英文，不含中文）和 `ww card --lang zh`（中文）
- **三段式关于我**：职业信任（TruthSoft 创始人、LeanCloud/TEKsystems、趣直播/Square Root、50+ 已交付项目，含猿辅导/粉笔/江苏卫视/DBS/HSBC）· 技术栈（Android/iOS、Vue/React/Angular、Java/Spring/Python、小型模型训练与推理、阿里云/AWS/Azure）· 个人简介与影响力（1995 年生于广州、NOIP 前 300、IELTS 6.5、BFU 辍学 / GDUFS 大专 / CSTU 硕士、16K+ 工程师、月浏览量约 10 万）
- **联系方式**（左侧面板）：TruthSoft · 邮箱 · 微信/WhatsApp · GitHub
- **高像素密度**：默认 4200×2400（2×），`--scale N` 1–8
- **暖色浓缩咖啡/焦糖主题**，与你的头像色调匹配（最近提交 `44b18b3`）

所有更改均已提交到 `main`。预览已打开——请查看，并告诉我接下来还需要什么，例如：

- 调整焦糖强调色（更浅/更深）
- 尝试浅奶油色主题
- 修改任一卡片上的文案
- 添加 `--theme` 选项以切换调色板

你可以运行的所有命令：

```bash
ww card --lang zh        # Chinese card
ww card --lang en        # English card
ww card --scale 3        # higher resolution
ww card avatar           # avatar only
```
