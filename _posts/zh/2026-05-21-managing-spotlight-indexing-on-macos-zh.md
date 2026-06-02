---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 管理macOS上的Spotlight索引
translated: true
type: note
---

您有几个选择，从温和到彻底：



    选项 A：立即停止峰值（稍后恢复索引）


    sudo mdutil -a -i off


    立即关闭所有卷的索引。`mdworker` 进程将结束并退出。索引保持关闭，直到您通过 `sudo mdutil -a -i on` 重新开启。

    选项 B：添加 Spotlight 排除项（推荐）

    在 系统设置 > Siri 与 Spotlight > 搜索隐私 中，拖入：
    - ~/Projects/ 或您的 `node_modules` 所在目录
    - ~/Library/Caches/
    - ~/Downloads/

    或通过命令行：

    sudo mdutil -E /
    sudo mdutil -i off /Users/lzwjava

    这会清除索引并停止索引您的主文件夹，同时保留系统范围的索引用于搜索。

    选项 C：永久关闭 Spotlight（不再有搜索）


    sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.metadata.mds.plist


    这会取消注册 Spotlight 守护进程，使其在重启后也永远不会再次启动。Cmd+Space 搜索将停止工作。您可以通过将 `unload` 替换为 `load` 来恢复。

    选项 D：仅终止当前占用资源的进程


    sudo pkill mdworker
    sudo pkill mds


    进程现在会终止，但在一分钟内会重新启动。这只是临时止血措施。



    我的建议：选项 B — 停止索引您的主文件夹。您仍可使用 Spotlight 搜索应用/系统，但它不会再爬取 node_modules、缓存或您庞大的 ~/Projects 目录树。每次重启后 250% 的 CPU 峰值将消失。

    需要我运行它吗？
