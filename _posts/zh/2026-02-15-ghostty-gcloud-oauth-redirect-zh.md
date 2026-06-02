---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ghostty 拦截 gcloud OAuth 重定向
translated: true
type: note
---

**Question:** 为什么在 Google 页面（localhost:83xx 重定向）点击“Yes”后，`gcloud auth login` 在 Ghostty 中会卡住，而在 macOS 的 iTerm 中却运行正常？

**Answer:**

这是一个已知的兼容性问题，发生在 macOS 上的某些较新或非主流的 terminal emulators（包括 Ghostty）中，主要是在处理诸如 `gcloud auth login` 之类工具的 OAuth loopback redirect 时出现。

Google Cloud SDK 会在一个随机的高端口（通常是 8085、8184，或者在你这种情况下的 8300 系列）启动一个微型 local web server，用于接收来自 browser 重定向的 authorization code。在你通过 Google 授权页面批准后，browser 会重定向到 `http://localhost:<port>/?code=...`，terminal 的 local server 需要接收该 HTTP request 才能完成 authentication。

在 iTerm（以及默认的 Terminal.app）中，这通常能可靠地工作，因为它们能正确允许传入的 loopback connections 且不会干扰 socket。而在 Ghostty 中，重定向往往无法到达 local server —— terminal 显得像是卡住了（无限等待），即便 browser 可能已经显示了成功页面或“connection refused”等错误。

### 常见原因及解决方法

1. **最快捷的规避方案（首选建议）**
   使用非浏览器流程：

   ```
   gcloud auth login --no-launch-browser
   ```

   这会打印出一个长 URL。将其复制并粘贴到 browser 中，批准后，将最终重定向的 URL（或显示的 code）复制回 terminal 提示符中。这会完全跳过 local server，在任何 terminal 中都有效。

2. **替代的一行命令流程（如果觉得上述方式繁琐）**

   ```
   gcloud auth application-default login --no-launch-browser
   ```

   （用于 ADC credentials —— 通常是开发者真正需要的），如果经常操作，可以结合脚本使用。

3. **其他检查/尝试项目**
   - 确保没有其他 process 占用特定端口（较罕见，因为端口是随机的）：

     ```
     lsof -i :83xx   # 如果能看到端口号，请替换为实际端口
     ```

   - 尝试临时更换默认 browser（有用户反馈 Safari 和 Chrome 表现不同，但这通常不是根本原因）。
   - 将 Ghostty 更新到最新版本 —— 较新的 build 有时会修复 loopback 处理或 child process I/O 的怪癖。
   - 如果愿意尝试，可以显式使用 `--browser` flag（虽然不太可能解决根源问题）：

     ```
     gcloud auth login --browser="/Applications/Safari.app"
     ```

4. **长期建议**
   这很可能是 Ghostty 特有的 bug（或者是 macOS socket/permissions 的交互问题）。你可以在 Ghostty 的 GitHub repo (mitchellh/ghostty) 中搜索或反馈该问题，并提供 macOS 版本、Ghostty 版本以及具体操作表现等细节 —— 类似的 localhost/socket 问题也出现在其他工具（如 GitHub CLI, Gemini CLI）中。

处于这种情况的大多数用户只需使用 `--no-launch-browser` 即可立即解决问题。

**References:**

- [https://stackoverflow.com/questions/71912626/gcloud-auth-login-localhost-redirect-failed](https://stackoverflow.com/questions/71912626/gcloud-auth-login-localhost-redirect-failed)
- [https://groups.google.com/g/google-cloud-sdk/c/-GLEhSaDHoM](https://groups.google.com/g/google-cloud-sdk/c/-GLEhSaDHoM)
- [https://github.com/google-gemini/gemini-cli/issues/2547](https://github.com/google-gemini/gemini-cli/issues/2547) (类似在 macOS 上的另一个 CLI 中 localhost OAuth 卡住的问题)
