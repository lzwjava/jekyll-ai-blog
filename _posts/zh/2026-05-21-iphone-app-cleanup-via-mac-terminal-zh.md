---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过Mac终端清理iPhone应用
translated: true
type: note
---

尚未连接，但一旦你插入 iPhone，我们可以利用 Mac 上已有的工具执行以下操作：

**可用工具**：`ideviceinstaller`（通过 Homebrew 安装的 libimobiledevice 工具包）

**清理 iOS 应用的工作流程：**

1. **列出所有用户安装的应用**——显示 bundle ID 和名称：
   ```bash
   ideviceinstaller -l -o list_user
   ```

2. **按 bundle ID 卸载不用的应用**：
   ```bash
   ideviceinstaller -U com.example.unused-app
   ```

3. **智能清理方案**——我可以编写一个脚本：
   - 从你的 iPhone 列出 200-300 个应用
   - 与最近未打开的应用交叉比对（遗憾的是 iOS 不通过此 API 提供最后使用日期）
   - 按排序/分组方式呈现供你决定
   - 按类别或逐个批量删除

这需要你在 iPhone 上**信任这台 Mac**（首次连接时会出现常见的“信任此电脑”提示）。完成后，我就可以将完整列表直接显示在终端中，让你选择要删除哪些应用。

要插入 iPhone 开始操作吗？