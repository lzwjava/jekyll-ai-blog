---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH仓库隧道迁移的优势
translated: true
type: note
---

以下是翻译结果：

```
SSH 仓库:  205  (87.6%)
HTTPS 仓库: 23  ( 9.8%)
其他:        7  ( 3.0%)
```

是的，你绝对需要这个修复。87.6% 的仓库通过 ncat SOCKS5 隧道连接。

好消息：macOS 自带的 `nc` 已经支持 SOCKS5：

```
nc -X 5 -x localhost:7891 %h %p
```

需要我现在就更新你的 `~/.ssh/config` 吗？当前配置：

```
ProxyCommand ncat --proxy localhost:7891 --proxy-type socks5 %h %p
```

将变成：

```
ProxyCommand nc -X 5 -x localhost:7891 %h %p
```

`nc` 使用原始的 `read()/write()`，没有 nsock 事件循环抽象层——对于大仓库的 `git pull` 等批量传输，I/O 路径更简单。无需安装，它已经在 `/usr/bin/nc` 中了。