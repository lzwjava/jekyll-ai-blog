---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在天翼网关上禁用 IPv6
translated: true
type: note
---

**Question:** 如何在 XGPON 天翼网关 (双频 WiFi 6) 上禁用 IPv6？

**Answer:**

## 如何在 XGPON 天翼网关 (双频 WiFi 6) 上禁用 IPv6

> ⚠️ **重要提示：** 天翼网关上的 IPv6 设置对普通用户账号是隐藏的。你 **必须使用超级管理员 (telecomadmin) 账号** 才能访问并修改 IP Mode 设置。机身背面标签上的普通账号仅提供基础/受限的访问权限。

---

### Step 1 — 以超级管理员身份登录

1. 通过 LAN 线或 WiFi 将电脑连接到网关。
2. 打开浏览器并访问：
   - `http://192.168.1.1` — 最常见地址
   - 或 `http://192.168.1.1:8080` — 部分型号使用（如 TEWA 系列）
3. 使用 **超级管理员凭据** 登录：
   - **用户名 (Username):** `telecomadmin`
   - **密码 (Password):** 通常为 `nE7jA%5m`（许多型号的默认密码 — 如果无效，请联系中国电信 / 10000 号获取您设备的超级管理员密码）

如果您没有使用超级管理员账号登录，界面中许多设置将被隐藏。

---

### Step 2 — 进入网络设置

1. 登录后，点击顶部菜单中的 **网络 (Network)**。
2. 点击 **网络设置 (Network Settings)**。
3. 在 **连接名称 (Connection Name)** 下，选择您的互联网连接 — 通常名称类似于：
   - `3_INTERNET_R_VID_XX` 或 `x_INTERNET_x_VID_xx`

---

### Step 3 — 将 IP 模式更改为仅 IPv4

在连接设置中，找到 **IP 模式 (IP Mode)** 下拉菜单。目前它可能被设置为 `IPv4&IPv6`。请将其更改为：

- **IPv4** (仅 IPv4)

这将禁用 WAN 连接上的 IPv6。

要完全禁用运营商分发的 IPv6，关键设置是在连接的 IP Mode 中选择 **IPv4**（而不是 IPv4&IPv6）。

---

### Step 4 — 保存并应用

1. 点击 **保存 (Save)** 或 **保存/应用 (Save/Apply)**。
2. 等待大约 10–15 秒让更改生效。
3. 如果有必要，请重启网关以确认设置已应用。

---

### Step 5 — 验证 IPv6 是否已禁用

在您的电脑上，打开 **Command Prompt** 并输入：

```
ipconfig
```

如果 IPv6 已成功禁用，您的网络适配器上应该 **不再显示** `240e:...` 格式的 IPv6 地址 — 应该只显示标准的 IPv4 地址。

---

### ⚠️ 注意事项

- **部分网关固件版本** 锁定了 IPv6 设置，即使使用超级管理员账号也不允许用户禁用。在这种情况下，您需要拨打 **中国电信 (10000)** 并要求他们在后台关闭您线路的 IPv6。
- 具体的菜单布局可能会因您的 XGPON 网关硬件型号（如 HG6143D, HG5143F, TEWA-208G 等）不同而略有差异。
- 如果您在网关下方还连接了一个 **下级路由器 (Router)**，您还应该分别在路由器的 WAN/LAN 设置中禁用 IPv6，以完全防止 IPv6 分配给您的本地设备。

---

References:

- [蓝胖子探索IPV6-接入篇-(001)天翼网关开启IPV6 - 博客园](https://www.cnblogs.com/lanhuxing/p/16907583.html)
- [电信的 IPv6 如何关闭 - V2EX](https://v2ex.com/t/551047)
- [新款天翼网关怎么设置 IPv6 - 知乎](https://www.zhihu.com/question/646319026)
- [个人宽带如何开启IPv6网络访问 - ipw.cn](https://ipw.cn/doc/ipv6/user/enable_ipv6.html)