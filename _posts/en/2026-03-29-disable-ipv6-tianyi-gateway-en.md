---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable IPv6 on Tianyi Gateway
translated: false
type: note
---

**Question:** How do I disable IPv6 on the XGPON Tianyi (天翼) Gateway (Dual-Band WiFi 6)?

**Answer:**

## How to Disable IPv6 on the XGPON 天翼 Gateway (Dual-Band WiFi 6)

> ⚠️ **Important Note:** IPv6 settings on Tianyi gateways are hidden from regular user accounts. You **must use the Super Administrator (telecomadmin) account** to access and change IP mode settings. The standard account on the back label only provides basic/limited access.

---

### Step 1 — Log In as Super Administrator

1. Connect your computer to the gateway via LAN cable or WiFi.
2. Open a browser and go to:
   - `http://192.168.1.1` — most common
   - Or `http://192.168.1.1:8080` — used by some models (e.g., TEWA series)
3. Log in with the **Super Admin credentials**:
   - **Username:** `telecomadmin`
   - **Password:** Usually `nE7jA%5m` (default for many models — if this doesn't work, contact China Telecom / 10000 to get your device's super admin password)

If you haven't logged in with the super administrator account, many settings will be hidden from the interface.

---

### Step 2 — Navigate to Network Settings

1. After logging in, click **网络 (Network)** in the top menu.
2. Click **网络设置 (Network Settings)**.
3. Under **连接名称 (Connection Name)**, select your internet connection — it is typically named something like:
   - `3_INTERNET_R_VID_XX` or `x_INTERNET_x_VID_xx`

---

### Step 3 — Change IP Mode to IPv4 Only

In the connection settings, look for the **IP模式 (IP Mode)** dropdown. It is likely currently set to `IPv4&IPv6`. Change it to:

- **IPv4** (IPv4 Only)

This disables IPv6 on the WAN connection.

To fully disable ISP-delivered IPv6, the key setting is to choose **IPv4 Only** in the connection's IP mode (rather than IPv4&IPv6).

---

### Step 4 — Save and Apply

1. Click **保存 (Save)** or **保存/应用 (Save/Apply)**.
2. Wait approximately 10–15 seconds for the change to take effect.
3. Reboot the gateway if necessary to confirm the setting is applied.

---

### Step 5 — Verify IPv6 is Disabled

On your PC, open **Command Prompt** and type:

```
ipconfig
```

If IPv6 is successfully disabled, you should **no longer see** a `240e:...` style IPv6 address on your network adapter — only the standard IPv4 address should appear.

---

### ⚠️ Caveats

- **Some gateway firmware versions** lock IPv6 settings and do not allow users to disable it, even with the super admin account. In that case, you need to call **China Telecom (10000)** and request they disable IPv6 on your line from the back end.
- The exact menu layout may vary slightly depending on your specific XGPON gateway hardware model (e.g., HG6143D, HG5143F, TEWA-208G, etc.).
- If you have a **downstream router** connected to the gateway, you should also disable IPv6 on the router's WAN/LAN settings separately to fully prevent IPv6 from being distributed to your local devices.

---

References:

- [蓝胖子探索IPV6-接入篇-(001)天翼网关开启IPV6 - 博客园](https://www.cnblogs.com/lanhuxing/p/16907583.html)
- [电信的 IPv6 如何关闭 - V2EX](https://v2ex.com/t/551047)
- [新款天翼网关怎么设置 IPv6 - 知乎](https://www.zhihu.com/question/646319026)
- [个人宽带如何开启IPv6网络访问 - ipw.cn](https://ipw.cn/doc/ipv6/user/enable_ipv6.html)
