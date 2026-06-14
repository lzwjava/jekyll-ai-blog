---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tailscale被代理位置误导
translated: true
type: note
---

**问题：** 总结网络诊断结果，隐去所有IP地址，并重点关注底部的关键发现。

**回答：**

## 网络诊断总结

### 设置
- **Mac**（父母家，广州A区）通过hysteria2代理（洛杉矶）连接以处理常规流量
- **`to`工作站**（你家，广州B区/增城）位于中国电信NAT后的本地子网中

### 路由问题
当前Tailscale路径：
```
Mac（广州A区）→ hysteria2代理（美国洛杉矶）→ DERP中继（新加坡）→ to工作站（广州B区）
```
延迟：平均约500毫秒，有时高达900毫秒。

### 关键发现（底部部分）
**真正的问题并非网络拓扑——而是Tailscale对Mac的位置判断错误。**

由于Mac通过洛杉矶的hysteria2代理路由所有流量，**Tailscale认为Mac位于美国**，因此选择新加坡作为最近的DERP中继。实际物理路径为：

```
广州 → 美国 → 新加坡 → 广州
```

两台位于**同一城市**的机器之间产生了完全不必要的跨洲往返。

如果Tailscale能识别Mac的真实IP（中国电信，广州），它会选择更近的中继——很可能是香港——从而大幅降低延迟，可能提升5-10倍。

### 根本解决方案
**在Mac上将Tailscale流量排除在hysteria2代理之外。** 让Tailscale使用真实的本地IP进行协调和DERP选择，而其他流量仍通过代理路由。