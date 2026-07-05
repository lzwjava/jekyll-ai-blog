---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 中文输入已成功配置
translated: true
type: note
---

完成。中文输入法现已**完全设置并正常工作**。以下是总结：

---

## 状态：已安装并配置完成

| 项目 | 状态 |
| ------ | ------ |
| **IBus** + **ibus-libpinyin** | 已安装 |
| **GNOME 输入源** | 已添加（`ibus libpinyin`） |
| **IBus 守护进程** | 正在运行 |
| **活动引擎** | `libpinyin` ✅ |

## 使用方法

**切换输入法**：`Super` + `Space`（或点击顶部显示“EN”的栏）

**输入拼音**：直接输入拼音如 `nihao` → 会出现候选词

**切换回英文**：再次按下 `Super` + `Space`

## 快速测试

打开任意文本应用（终端、浏览器等）并输入。拼音引擎现已生效。

---

无需安装步骤——你的 Ubuntu 24.04 上已具备所有组件。libpinyin IBus 引擎已添加为输入源，但未激活。我已将其设置为 `libpinyin`，现在可以通过 GNOME 输入菜单进行切换。
