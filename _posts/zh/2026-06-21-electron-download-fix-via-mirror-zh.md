---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Electron 下载镜像修复
translated: true
type: note
---

一切正常：

- **镜像可达** —— `npmmirror.com` 通过你的代理快速返回 `HTTP/2 302`（重定向至二进制文件），而直连 GitHub 则会卡住。
- **npm 正常传递配置** —— `npm config get electron_mirror` 返回了正确的值，因此 Electron 的 postinstall 脚本会读取 `npm_config_electron_mirror` 并从镜像下载。（`Unknown user config` 警告无害——npm 仍会将此设置传递给生命周期脚本；这只是未来 npm 主版本弃用该功能的提示。）

## 总结

**卡住的原因：** `hermes update` → “正在更新 Node.js 依赖” → `npm ci` → Electron 的 `install.js` 的 postinstall 脚本尝试**直接从 GitHub**（绕过了你的 `localhost:7890` 代理）下载约 100 MB 的二进制文件。由于直连 GitHub 卡住，`npm ci` 始终未返回，Python 更新器在 `subprocess.wait()` 中阻塞——这正好对应你 Ctrl-C 回溯中出现的位置。

**我已执行的操作：**

1. 终止了残留的 `node install.js` / `npm ci` 进程，并删除了空的 `electron-download-*` 临时目录。
2. 创建了 `~/.npmrc` 文件，将 Electron（及 electron-builder 二进制文件）的下载源指向快速的 `npmmirror.com` 镜像。
3. 确认该镜像可达，且 npm 已将该配置传递给 postinstall 脚本。

**下一步 —— 只需重新运行更新：**

```
hermes update
```

现在“正在更新 Node.js 依赖”这一步应该能顺利通过，因为 Electron 二进制文件将从镜像下载，而不会在 GitHub 上卡住。如果你愿意，我可以立即手动运行 `npm ci` 步骤，以确认下载端到端完成，然后你再执行 `hermes update`——请告诉我。
