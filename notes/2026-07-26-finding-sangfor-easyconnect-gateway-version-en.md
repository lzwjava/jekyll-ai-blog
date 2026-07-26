---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding Sangfor EasyConnect Gateway Version
translated: false
type: note
---

Question: **How can I know the Sangfor EasyConnect VPN gateway version?**

Answer:

The **gateway version is the Sangfor SSL VPN server version**, not the EasyConnect client version. Usually only the company VPN administrator knows it, but you can find it in several ways.

## Method 1: Check the EasyConnect login page (easiest)

Open your company VPN URL:

```
https://vpn.company.com
```

Before login, look for:

* footer text
* "About"
* "System Information"
* "版本信息"
* "Sangfor SSL VPN"
* "aTrust"

Examples:

```
Sangfor SSL VPN M7.6.7
```

or

```
深信服SSL VPN 7.6.7
```

---

## Method 2: Check downloaded client package

When you download EasyConnect from the company VPN portal, the portal often embeds the server version.

After downloading:

Windows:

```
EasyConnectSetup.exe
```

Right click:

```
Properties
 → Details
```

Look for:

```
Product version
```

or:

```
File version
```

Example:

```
7.6.7.12345
```

---

## Method 3: Browser developer tools

Open the VPN login page.

Press:

```
F12
→ Network
→ Refresh page
```

Look at requests/responses.

Search for:

```
version
product
release
M7
```

Sometimes you see:

```
serverVersion=M7.6.7
```

---

## Method 4: Ask the VPN admin

The admin console usually shows:

```
系统管理
  ↓
系统信息
  ↓
版本信息
```

Example:

```
SSL VPN
Version:
M7.6.7R1
Build:
xxxx
```

---

## Method 5: Try the newest client

For your case (Windows 11 x64):

Install:

```
EasyConnect M7.6.7+
```

If the gateway is older, usually you will see an error like:

```
客户端版本过高，请下载对应版本客户端
```

or:

```
不支持当前服务端版本
```

If it logs in successfully, compatibility is OK.

---

Given your previous issue ("EasyConnect crashes a lot on Windows 11"), I would first check:

1. Open company VPN URL in Edge/Chrome.
2. Look at the login page footer/version.
3. If nothing appears, install **M7.6.7+ x86 Windows client**.

The client can usually talk to older M7.x gateways, but very old gateways (especially pre-M7.1) are where Windows 11 compatibility problems appear.
