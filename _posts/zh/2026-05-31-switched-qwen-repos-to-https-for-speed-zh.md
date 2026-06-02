---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已将 Qwen 仓库切换至 HTTPS 以提升速度
translated: true
type: note
---

已完成。所有5个Qwen仓库已切换为HTTPS。总结：

**根本原因：** 将`ncat`用作SSH代理命令时，大数据传输速度较慢。SOCKS5代理本身（mihomo，端口7891）速度较快（约1 MB/s），但ncat的双向隧道为git包文件增加了开销。

**已应用修复：** 所有Qwen仓库现在使用HTTPS，该协议通过mihomo的HTTP代理（端口7890）传输。已验证运行正常——`Qwen2.5-Coder`的获取操作在约77秒内完成了413个对象的下载。

**额外提示：** 你的`.git`目录中有1.38 GiB的垃圾数据。建议运行：
```
git -C /Users/lzwjava/projects/Qwen2.5-Coder gc --prune=now
```

对于未来的仓库：如果从GitHub克隆模型仓库，默认使用HTTPS——对于大文件传输，HTTP代理比SSH隧道更快。
