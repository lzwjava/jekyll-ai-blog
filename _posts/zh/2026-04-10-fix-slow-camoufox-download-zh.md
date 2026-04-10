---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Camoufox下载速度慢的问题
translated: true
type: note
---

问题：为什么 `npx camoufox-js fetch` 进度开始移动后仍然极其缓慢（完成1%，剩余时间约50,000秒）？

答案：

这意味着下载**正在工作**，但你与 Camoufox 二进制文件服务器的连接**极其缓慢**。预估剩余时间 `50606.8s`（约14小时）是基于**当前的传输速度**计算得出的，可能只有几 KB/s。

这种情况通常由以下原因之一导致：

---

## 1. 你仍在使用代理（最可能的情况）

即使你已经移除了 `proxychains4`，你的系统可能仍在使用：

* SOCKS 代理（Clash / V2Ray / Shadowsocks）
* HTTP 代理（`HTTP_PROXY`、`HTTPS_PROXY`）
* 出口节点缓慢的 VPN
* 公司网络过滤

快速检查：

```bash
env | grep -i proxy
```

如果看到类似以下内容：

```
HTTP_PROXY=...
HTTPS_PROXY=...
ALL_PROXY=...
```

那么你**仍在通过代理下载** → 速度非常慢。

修复：

```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
npx camoufox-js fetch
```

---

## 2. Node.js 下载器是单线程的

`camoufox-js fetch` 使用 Node fetch 进行下载 → **单一连接**
大文件 + 遥远的 CDN = 速度非常慢。

这在以下情况中很常见：

* 服务器位于美国/欧盟
* 你通过亚洲代理路由
* 数据包丢失率高

---

## 3. Camoufox 二进制文件体积大

Camoufox 下载内容包括：

* 打过补丁的 Firefox
* 隐身补丁
* 沙盒运行时
* 平台特定的捆绑包

通常为 **150MB–400MB**

以 **10 KB/s** 的速度下载：

```
300MB / 10KB/s ≈ 8 小时
```

你的预估剩余时间（约14小时）与此相符。

---

## 4. 最佳修复方法（推荐）

取消并强制进行直接快速下载：

```
Ctrl + C
```

然后：

```
NO_PROXY=* npx camoufox-js fetch
```

或：

```
npm_config_proxy= npm_config_https_proxy= npx camoufox-js fetch
```

---

## 5. 更好的方法（最快的方法）

使用 **curl 多线程下载**手动操作：

首先找到 URL：

```
DEBUG=camoufox* npx camoufox-js fetch
```

它将打印类似以下内容：

```
Downloading from https://github.com/.../camoufox-mac.zip
```

然后使用以下命令下载：

```
curl -L -o camoufox.zip <URL>
```

然后解压到缓存目录：

```
~/.cache/camoufox/
```

这比原方法**快10倍**。

---

## 6. 如果你正在安装 Hermes agent

在 fetch 完成后：

```
cd hermes-agent
npm install
npm run build
```

或：

```
pnpm install
pnpm dev
```

Hermes 本身很小 —— **Camoufox 是主要的大文件部分**。

---

## 预期的正常速度

健康的下载应该看起来像：

```
Downloading Camoufox... [======----------------------] 15% 20s
```

而不是：

```
1% 50606s
```

所以你的连接速度**比正常情况慢了约1000倍**。

---

## 快速诊断（运行此命令）

```
curl -I https://github.com
```

如果耗时 >2s → 你的 GitHub/CDN 路由很慢。

---

## 最可能的原因（按可能性排序）

1. 代理仍处于启用状态（90%）
2. VPN 出口节点缓慢
3. GitHub CDN 被屏蔽/所在地区访问缓慢
4. 数据包丢失 / DNS 问题
5. ISP 对大文件下载进行限流

---

## 最快的解决方案

使用手机热点（认真的）：

```
切换 wifi → 手机热点
npx camoufox-js fetch
```

通常能在 **30秒** 内完成。