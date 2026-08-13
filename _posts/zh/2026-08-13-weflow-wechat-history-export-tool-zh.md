---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'WeFlow: 微信历史导出工具'
translated: true
type: note
---

**问题：什么是 WeFlow，这款微信聊天记录导出工具？**

**回答：** WeFlow 是一款完全本地化、开源（Electron + React + TypeScript）的工具，用于实时查看、分析和导出微信聊天记录。它支持微信 4.0 及以上版本，能够直接读取微信客户端本地的 SQLite/MSG 数据库文件（Windows/macOS/Linux），无需 root 权限，无需云端上传。

**工作原理：**
- 直接从磁盘读取微信客户端的本地 SQLite/MSG 数据库文件（Windows/macOS/Linux）——无需 root，无需云端上传。
- 通过直接读取 Windows 微信客户端本地的数据库文件（MSG 文件）来获取所有聊天记录——文本、图片、贴纸、文件——并让你能够按联系人、群组或时间范围筛选，导出为结构化的 HTML 存档。
- 能够解密聊天中的图片、视频和 Live Photos（仅限使用 Google Live Photos 协议拍摄的），支持修改/删除本地消息，并实时刷新新消息，无需生成中间解密数据库。
- 声称“零网络权限”——从数据库解密到渲染全部在本地完成，不产生任何外连请求。

**仓库状态——在 `git clone` 前值得了解：**
原始仓库（`hicccc77/WeFlow`）收到了腾讯律师（MSK 律所）依据 DMCA 1201 条款发出的下架通知，理由是绕过了微信的数据库加密（“复杂技术”）。README 现在讽刺性地记录了此事，指出该项目不包含任何破解/解密/逆向工程代码，并且使用该工具打开未加密的 SQLite 文件所产生的任何“数据可视化现象”并非开发者的责任。下架后出现了像 `jacklilyhello/WeFlow` 和 `chency7/WeFlow` 这样的分支——在依赖之前请检查哪个分支是真正得到维护的，因为原始作者的联系信息已因隐私原因被清除。

**如果你以编程方式实现（更符合你偏好 CLI 的工作流程）：** Windows/macOS 上的微信将消息存储在加密的 SQLite 数据库中；密钥派生和表结构正是这类工具逆向工程的对象。对于 Android，还有 `wechat-dump`（需 root 的手机 + adb），它从已 root 的 Android 手机解析微信消息，并将其渲染为自包含的 HTML 文件，包括语音消息、图片、表情和视频——如果你想将聊天记录输入 LLM 管道，它比 WeFlow 的 GUI 更具脚本化能力。

**参考资料：**
- [chency7/WeFlow](https://github.com/chency7/WeFlow)
- [hicccc77/WeFlow（原始仓库，已遭 DMCA 下架）](https://github.com/hicccc77/WeFlow)
- [jacklilyhello/WeFlow（分支）](https://github.com/jacklilyhello/WeFlow)
- [ppwwyyxx/wechat-dump（Android，可脚本化）](https://github.com/ppwwyyxx/wechat-dump)