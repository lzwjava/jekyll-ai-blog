---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 各国5G SA部署情况
translated: true
type: note
---

**问题：** 目前有哪些国家和公司部署了 5G 独立组网（SA）网络？  
**答案：**

以下是截至 2026 年中的全球概览：

---

## 全球 5G SA 部署现状

截至 2025 年 4 月，65 个国家的 163 家运营商正在投资公共 5G SA 网络，其中 39 个国家的 73 家运营商已推出或软推出相关服务。但覆盖范围和质量差异巨大。

---

## 各区域领先者

### 🇨🇳 中国 —— SA 已推出，但你可能并未接入
这对你来说至关重要。截至 2021 年 11 月，中国移动、中国联通和中国电信均已实现 5G SA 网络的大规模部署，SA 核心网已投入运营。中国移动运营着全球最大、集中化、全云化、全融合的 5G SA 核心网。

**那么为什么你仍然在使用 NSA？** 你的 CGNAT 证据很有说服力——你的热点（iPhone 个人热点）很可能未被配置为 SA 模式，或者你所在的特定基站尚未完成迁移。中国确实存在 SA 核心网，但设备、SIM 卡和基站三者必须协同工作。

### 🇺🇸 美国
T-Mobile US 是 2025 年之前中国以外少数几个大规模部署 SA 的知名运营商之一。AT&T 和 Verizon 的进展相对较慢。

### 🇩🇪 欧洲 —— 德国领先
德国三大全国性移动网络运营商现已推出 5G SA 服务——德国电信于 2025 年 7 月宣布实现全国 5G SA 覆盖，沃达丰也启动了全国范围的 SA 服务，O2 Telefónica 则推出了“5G Plus”服务。

### 🇪🇸 西班牙
Telefónica（Movistar）利用 700 MHz 和 3.5 GHz 频谱，通过其“5G+”SA 网络覆盖了 5,700 个市镇中超过 94% 的人口。

### 🇦🇪 阿联酋 / GCC —— 性能领先者
海湾合作委员会（GCC）已成为全球 5G SA 性能的领先者。阿联酋达到 1.24 Gbps 的 SA 中位数下载速度——即便与全光纤宽带相比也表现卓越。

### 🇰🇷 韩国
KT 是目前唯一一家拥有完全运营的全国性独立组网核心网的运营商。韩国政府已要求在 2026 年前将所有 5G 基站接入独立组网核心设备。

### 🇮🇳 印度
Reliance Jio 是中国以外少数几个大规模部署 SA 的运营商之一。

---

## 全球实际情况

从全球来看，基于 Speedtest 样本份额的 5G SA 可用性在 2025 年第四季度仅为 17.6%——全球约六分之一的 5G 速度测试发生在独立组网网络上。因此，即使在某些地区 SA 已“部署”，大多数用户实际上并未使用。

---

## 这对你的具体含义

中国拥有 SA 基础设施，但你的热点很可能并未接入，原因如下：

1. **iPhone 个人热点**——即使你的直接连接是 SA 模式，调制解调器在热点模式下也可能回退到 NSA
2. **基站迁移进度**——广州并非所有基站都已完成 SA 迁移
3. **SIM 卡配置**——中国电信 SA 可能要求特定的套餐/APN 配置

要实际验证：在 iPhone 上进入工程模式（拨打 `*3001#12345#*` 然后点击呼叫），查看 NR 连接类型。在小区信息中查找 `NR SA` 或 `NR NSA`。中国移动、中国电信和中国联通是 5G SA 的早期采用者，并且已经推出了 5G-Advanced——因此你所在运营商的 SA *确实存在*，你只需要确认你的特定基站和 SIM 卡是否已接入。

参考来源：
- [5G Standalone State of Play — Opensignal Feb 2026](https://insights.opensignal.com/2026/02/5g-standalone-state-of-play-architecture-deployed-monetisation-pending/dt)
- [Global Reality Check on 5G SA 2026 — Ookla/Omdia](https://www.communicationstoday.co.in/a-global-reality-check-on-5g-sa-and-5g-advanced-in-2026-ookla/)
- [GSA 5G Standalone April 2025](https://gsacom.com/paper/5g-standalone-april-2025/)