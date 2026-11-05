---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 删除微信链接语法
translated: true
type: note
---

已修复 ✅

**改动内容：**

| 位置 | 原来 | 现在 |
| --- | --- | --- |
| 第 255–262 行 | `[我能如何帮助你](#我能如何帮助你)` 等 8 个锚点链接 | 纯文本列表（去掉链接语法） |
| 第 272 行 | `https://lzwjava.com/english-en` | `lzwjava.com/english-en`（去掉协议头） |
| 第 274 行 | `https://lzwjava.com` | `lzwjava.com`（去掉协议头） |
| 第 516 行 | `https://github.com/lzwjava` | `github.com/lzwjava`（去掉协议头） |

**原理：** mdnice 按 CommonMark 渲染，`https://...` 裸链接会被自动识别成 `<a href>` 超链接；`[文字](#锚点)` 也会生成 `<a>` 标签。微信编辑器检测到这些非 `mp.weixin.qq.com` 域名的链接就报错。去掉协议头后这些只是普通文本，不会再生成链接，信息仍然保留给读者看。

已全文复查：`grep` 确认不再有任何 `https://`、`www.` 或 `](#` 链接语法。现在重新复制到 mdnice → 微信编辑器就不会再报"请勿插入非 mp.weixin.qq.com 域名的链接"了。