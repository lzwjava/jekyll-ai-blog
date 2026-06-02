---
audio: false
generated: true
lang: zh
layout: post
title: LaTeX 中的可配置字体
translated: true
type: note
---

你可以通过在 LaTeX 文档开头创建变量来实现字体可配置化。以下是几种实现方案：

## 方法一：简单变量定义（推荐）

## 方法二：使用条件语句适配不同系统

接下来我将创建一个支持自动操作系统检测的增强版本：

## 方法三：使用独立配置文件

您还可以创建独立的字体配置文件：
然后在主文档中调用：

## 常用 Linux 字体替代方案

以下是一些适用于 Linux 系统的优质字体替代方案：

**中文字体选项：**

- `Noto Sans CJK SC`（推荐）
- `Source Han Sans SC`
- `文泉驿微米黑`
- `Droid Sans Fallback`

**英文字体选项：**

- `Liberation Serif`（Times New Roman 替代方案）
- `DejaVu Serif`
- `Linux Libertine`
- `TeX Gyre Termes`

## 使用指南

1. **方法一**最为简单——需要时直接取消 Linux 字体行的注释即可
2. **方法二**允许您仅通过修改变量 `\fontsystem` 即可在不同系统间切换
3. **方法三**将字体配置独立保存，便于维护不同版本

请根据您的工作流程选择最合适的配置方案！
