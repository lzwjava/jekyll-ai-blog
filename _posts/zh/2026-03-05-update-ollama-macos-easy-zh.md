---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 轻松在 macOS 上更新 Ollama
translated: true
type: note
---

**在 macOS 上，更新 Ollama 通常非常简单**，因为官方安装包含自动更新。

### 最常见且推荐的方式（官方 .dmg / App 安装）

1. 在菜单栏中查找 **Ollama 图标**（屏幕右上角，靠近时钟、Wi-Fi、电池图标等）。
   它通常看起来像一个小蓝色的 Ollama 标志或风格化的“O”。

2. 点击 Ollama 菜单栏图标

3. 如果有更新可用，您通常会看到类似以下内容：
   - "Update available"
   - "Restart to update"
   - "Install update"
   或类似文字

4. 点击 **"Restart to update"**（或等效按钮）
   → Ollama 将自动退出并使用新版本重新启动。

这是 Ollama 文档（截至 2026 年）中官方推荐的方法。

### 替代方法：强制手动更新 / 全新安装

- 前往 → <https://ollama.com/download>
- 下载最新的 macOS **Ollama.dmg**
- 打开 .dmg 文件
- 将新的 Ollama.app 拖到 /Applications/（询问时替换旧版本）
- 重新启动 Ollama

您的模型和配置保持安全（它们位于 `~/Library/Application Support/Ollama` 或 `~/.ollama`）。

### 快速版本检查

打开 Terminal 并运行：

```bash
ollama --version
# or
ollama -v
```

更新后，您应该看到更新的版本号。

### 注意事项 / 不常见情况

- **如果您通过 Homebrew 安装** (`brew install ollama` 或 `brew install --cask ollama`)：
  → `brew upgrade ollama` 或 `brew upgrade --cask ollama`
  （不过大多数人使用官方 .dmg 安装程序，而不是 Homebrew）

- 没有自动更新图标？
  → 确保 Ollama 在后台运行
  → 或者直接进行手动 .dmg 重新安装（非常安全）

基本上就是这样——macOS 用户通常在所有平台中获得最简单的更新体验。😄

如果您没有看到菜单栏图标或遇到任何特定错误，请告诉我！
