---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在 macOS 上安装 Chromium 浏览器
translated: true
type: note
---

是的，macOS 完全可以安装 Chromium 作为 Google Chrome 的替代品。Chromium 是 Chrome 所基于的开源基础，因此功能非常相似，但缺少一些专有的 Google 功能，如自动更新和某些编解码器。

### 如何安装

有几种简单的方法：

1. **通过 Homebrew（对大多数用户来说最简单）**：
   - 如果尚未安装 Homebrew，请先安装：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`。
   - 然后运行：`brew install --cask chromium`。
   - 此方法适用于 Intel 和 Apple Silicon（M1/M2/M3）芯片的 Mac。

2. **直接下载**：
   - 访问 Chromium 官方网站，下载适用于 Mac 的最新版本。
   - 解压后将应用程序拖到“应用程序”文件夹中。

3. **适用于开发者或自定义构建**：
   - 使用 Woolyss 等工具获取预构建版本，或在需要时从源代码构建（需要 Xcode）。

安装完成后，您可以在“系统设置”>“桌面与程序坞”>“默认网页浏览器”中将 Chromium 设置为默认浏览器。

[下载 Chromium](https://www.chromium.org/getting-involved/download-chromium/)
[Homebrew Formula](https://formulae.brew.sh/cask/chromium)
[在 Apple Silicon 上安装](https://dev.to/pixelrena/installing-chromium-on-mac-apple-m2-pro-tutorial-4i4i)
[MacUpdate 下载](https://chromium.macupdate.com/)
[最新版本](https://chromium.woolyss.com/download/en/)
