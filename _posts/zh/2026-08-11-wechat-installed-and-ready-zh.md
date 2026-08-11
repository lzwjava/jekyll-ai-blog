---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微信已安装并准备就绪
translated: true
type: note
---

完成！✅ WeChat 已安装并准备就绪。

**总结：**
- **包：** `wechat` 版本 **4.1.1.8** 已通过 dpkg 安装
- **缺失依赖已修复：** 已安装 `libxcb-icccm4`、`libxcb-image0`、`libxcb-render-util0`、`libxcb-keysyms1`（WeChat 所需的 Qt xcb 库）
- **验证：** `dpkg -s wechat` 显示 `install ok installed`，所有库均解析成功

您可以通过以下命令启动：
```bash
wechat
```
或者从应用程序启动器中搜索“微信”/WeChat。