---
audio: false
generated: true
image: false
lang: zh
layout: post
title: iPhone应用审计与清理摘要
translated: true
type: note
---

以下是本次会话的内容：

1. **检查已安装的应用** — 使用 `ideviceinstaller` 列出了已连接 iPhone "lzwjava" 上的 250 多个用户应用

2. **识别游戏** — 仅找到 6 个与游戏相关的应用（Chess、NeuralPlay Bridge、Mahjong 4 Friends、Vita Mahjong、Steam、Nintendo Switch App）

3. **删除 4 个游戏** — 通过 `ideviceinstaller uninstall` 卸载了 Mahjong 4 Friends、Vita Mahjong、Chess 和 NeuralPlay Bridge

4. **检查应用文件大小** — 获取所有应用的 `StaticDiskUsage`，从大到小排序。占用空间最大的应用：WeCom（852 MB）、TikTok（805 MB）、QQ（758 MB）、HSBC HK（749 MB）、WeChat（744 MB）

5. **列出最小的应用** — 展示了最小的 50 个应用（均小于 60 MB），并指出删除小应用不会释放太多空间——应优先删除大应用

游戏删除后释放的总空间：约 27 MB（微不足道）。真正节省空间的办法是删除像 HUAWEI AI Life（730 MB）、T-Life（570 MB）、Amazon Alexa（414 MB）等未使用的大应用。
