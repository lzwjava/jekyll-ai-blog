---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Cisco AnyConnect网络访问管理器概述
translated: true
type: note
---

Cisco AnyConnect 安全移动客户端是一套软件模块组合，提供安全的 VPN 接入、网络安全及基于策略的终端功能。该套件中的可选模块之一为 **Cisco 网络接入管理器（NAM）**。

### Cisco AnyConnect NAM 的功能
- **网络连接管理**：NAM 可取代 Windows 原生无线与有线网络管理器，负责配置、连接并保障有线与无线网络的安全。
- **高级 802.1X 支持**：为有线与无线网络连接提供全面的 **802.1X 认证**（EAP-TLS、PEAP、EAP-FAST 等），常用于需要证书认证或终端状态检测的企业环境。
- **策略强制执行**：管理员可定义策略以控制终端设备连接网络的方式——优先满足安全要求、限定允许连接的 SSID，或阻止不安全连接。
- **跨平台一致体验**：通过集中管控实现用户在不同 PC 设备上获得统一的网络接入体验。

### 重要说明
- **平台支持**：历史上 NAM 仅支持 Windows 系统。随着原生操作系统网络管理器（Windows Native Wi-Fi、macOS 客户端等）功能日益完善，思科自 AnyConnect v4.9 及后续版本起已停止对 NAM 的支持。
- **典型应用场景**：主要部署于企业、高校或政府网络，用于在系统登录前或登录过程中通过证书认证方式安全接入 Wi-Fi 或有线局域网。

👉 简而言之：**Cisco AnyConnect NAM（网络接入管理器）** 是一款高级网络连接管理器，可取代 Windows 原生客户端，通过 802.1X 认证和企业定制策略来管理有线/无线安全连接。

---

需要我进一步说明 **NAM 与更常用的 AnyConnect VPN 模块的关联与区别**吗？（因为目前大多数用户仅了解 VPN 功能部分）
