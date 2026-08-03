---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Markdown PDF浏览器启动错误
translated: true
type: note
---

此错误表示 Markdown PDF 扩展无法启动浏览器（Chromium/Edge）来生成 PDF。以下是几种解决方法：

## 解决方案 1：手动设置 Chromium 可执行文件路径（推荐）

1. 打开 VS Code 设置：
   - 按 `Ctrl + ,`（Windows/Linux）或 `Cmd + ,`（Mac）
   - 或者进入 文件 → 首选项 → 设置

2. 搜索 `markdown-pdf.executablePath`

3. 设置 Chrome/Edge 可执行文件的路径：

   ```json
   {
     "markdown-pdf.executablePath": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
   }
   ```

   或者如果你有 Chrome：

   ```json
   {
     "markdown-pdf.executablePath": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
   }
   ```

## 解决方案 2：禁用系统 Chrome 并使用内置 Chromium

1. 在 VS Code 设置中，搜索 `markdown-pdf.executablePath`

2. 将其设置为空字符串或删除该设置：

   ```json
   {
     "markdown-pdf.executablePath": ""
   }
   ```

3. 同时确保 `markdown-pdf.chromium.autoDownload` 设置为 `true`（在你的日志中显示为 true）

4. 重启 VS Code —— 它应该会自动下载 Chromium

## 解决方案 3：正确安装 Chrome/Edge

确保你已安装可用的浏览器：

- **Microsoft Edge** 已在 `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` 检测到
- 如果 Edge 已安装但无法正常工作，请尝试重新安装

## 解决方案 4：检查权限和 PATH

以管理员身份运行 PowerShell 并执行：

```powershell
# 检查 Edge 是否存在
Test-Path "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 如果未找到，尝试 Chrome
Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## 解决方案 5：使用其他 PDF 扩展

如果以上方法均无效，可考虑使用替代扩展：

- **vscode-pdf**
- **PDF Preview**
- 或者使用命令行工具如 `pandoc` 或 `wkhtmltopdf`

## 快速修复：修改 settings.json

将此内容添加到 VS Code 的 `settings.json` 中（使用 `Ctrl+Shift+P` → "首选项: 打开设置 (JSON)"）：

```json
{
  "markdown-pdf.executablePath": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "markdown-pdf.chromium.autoDownload": false
}
```

应用任一解决方案后，重启 VS Code 并再次尝试转换。最可能的修复方法是解决方案 1 —— 显式设置 Edge 可执行文件路径。
