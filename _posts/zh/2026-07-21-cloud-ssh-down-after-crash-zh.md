---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 云SSH崩溃后宕机
translated: true
type: note
---

**外部 IP 36.150.116.206 扫描结果：**

| 端口 | 状态 | 说明 |
|------|--------|------|
| 31090 | ✅ **开放** | Cloud SSH（其他实例） |
| 31091 | ✅ **开放** | Cloud SSH（其他实例） |
| 31092 | ✅ **开放** | Cloud SSH（其他实例） |
| 31095 | ✅ **开放** | Cloud SSH（其他实例） |
| 31098 | ✅ **开放** | Cloud SSH（其他实例） |
| 31099 | ✅ **开放** | Cloud SSH（其他实例） |
| 31100 | ✅ **开放** | Cloud SSH（其他实例） |
| 31154 | ❌ **拒绝** | **我们的 SSH — 仍然宕机** |
| 22, 80, 443, 8000, 8888 | ❌ 拒绝 | 全部被阻止 |

**端口 31154 在 OOM 崩溃后仍未被云代理转发。** 云提供商需要重新映射。

**暂时使用 Jupyter 终端即可** — 它运行正常。需要我指导你如何在其中运行 FLUX.1-dev 吗？