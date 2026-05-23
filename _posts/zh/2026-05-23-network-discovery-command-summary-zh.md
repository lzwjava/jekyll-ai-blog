---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络发现命令摘要
translated: true
type: note
---

所有 4 个表面均已更新并通过测试。以下是总结：

**命令：`ww network discover`**

```
ww network discover              # 快速：ARP 表 + MAC OUI 厂商查询
ww network discover -r           # + 反向 DNS 主机名
ww network discover -p           # + 端口探测 + 设备类型猜测
ww network discover -r -p        # 完整发现
ww network discover -s 10.0.0.0/24  # 自定义子网
```

**功能说明：**
1. 通过 UDP socket 技巧获取本地 IP（不发送流量）
2. 解析 `arp -an` 表（数字格式，无 DNS 超时）
3. 使用 MAC OUI 补充厂商名称（Apple、Xiaomi、TP-Link、Espressif 等）
4. `-r`：反向 DNS 主机名解析
5. `-p`：探测 8 个常用端口（SSH、HTTP、mDNS、VNC、AirPlay、iPhoneSync）→ 猜测设备类型
6. 过滤多播/广播，按 IP 排序
7. 打印对齐表格

**更改的文件：**
- `/Users/lzwjava/projects/ww/ww/network/discover.py` — 新模块
- `/Users/lzwjava/projects/ww/ww/main.py` — 调度 + 帮助文本（3 处）
- `/Users/lzwjava/projects/ww/README.md` — 命令表格行
- `/Users/lzwjava/projects/ww/completions/_ww` — zsh 补全条目