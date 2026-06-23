---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod 知识产权所有权揭秘
translated: true
type: note
---

=== IP 调查：213.173.102.150 ===

地理位置与所有者
  IP：         213.173.102.150
  城市：       罗马尼亚，蒂米什瓦拉
  ASN：        AS202779 — EVOBITS Information Technology SRL
  公司：       evobitsit.com（罗马尼亚，克卢日-纳波卡）
  业务：       云VPS、专用服务器、托管、私有云
  数据中心：   罗马尼亚境内 1.2MW + 3.5MW 设施（120 个机架、2N 电源）

相邻 IP（213.173.102.0/24 — 均为 EVOBITS）
  .130  → EVOBITS | 蒂米什瓦拉
  .140  → EVOBITS | 蒂米什瓦拉
  .145  → EVOBITS | 蒂米什瓦拉
  .148  → EVOBITS | 蒂米什瓦拉
  .149  → EVOBITS | 蒂米什瓦拉
  .150  → EVOBITS | 蒂米什瓦拉  ← 你的 Pod
  .151  → EVOBITS | 蒂米什瓦拉
  .152  → EVOBITS | 蒂米什瓦拉
  .155  → EVOBITS | 蒂米什瓦拉
  .160  → EVOBITS | 蒂米什瓦拉
  .170  → EVOBITS | 蒂米什瓦拉
  .200  → EVOBITS | 蒂米什瓦拉
  .240  → EVOBITS | 蒂米什瓦拉

更广泛的 EVOBITS 范围
  213.173.96.0/20  → 均为 EVOBITS，蒂米什瓦拉
  213.173.112.0/20 → 均为 EVOBITS，克卢日-纳波卡

NMAP 扫描（213.173.102.150）
  22/tcp    开放     ssh          ← 标准端口上的直连 SSH
  10000/tcp 开放     webmin?      ← 管理面板
  33880/tcp 已过滤（你通过 RunPod 映射的端口，当前不可用）

RunPod 分析
  RunPod 没有 ASN（bgp.tools 上无 BGP 记录）
  RunPod 不拥有任何 IP 地址段
  RunPod 是一个市场/平台，而非 ISP
  社区云 Pod 会暴露贡献者的真实公网 IP
  RunPod 文档确认："社区云的公共 IP 可能在 Pod 迁移时发生变化"——这意味着它是宿主机的 IP，而非 RunPod 的 IP

结论
  213.173.102.150 并非 RunPod 分配的 IP。
  它属于 EVOBITS（罗马尼亚托管公司）。
  EVOBITS 的某位客户（或 EVOBITS 自身）正在将其 RTX 2000 Ada GPU
  贡献到 RunPod 的社区云市场中。
  RunPod 将此机器上的端口 33880 映射为 22（SSH）供你使用。
  该机器很可能是 EVOBITS 蒂米什瓦拉数据中心内的一台虚拟机或裸金属服务器。

简而言之：RunPod 为你提供了一个 Pod ID 和代理地址，但底层 IP 是贡献者自己的——一家名为 EVOBITS 的罗马尼亚托管公司，拥有真实数据中心。该贡献者通过 RunPod 的点对点市场出租其 GPU。当 Pod 处于活动状态时，RunPod 将端口 33880 映射到该机器的 SSH 端口 22。当 Pod 暂停或停止时，该映射消失（连接被拒绝），但机器本身可能仍在运行（端口 22 和 10000 目前仍处于开放状态——那是其他人的服务器）。
